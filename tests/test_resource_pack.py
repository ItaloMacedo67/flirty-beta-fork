import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK_META = ROOT / "pack.mcmeta"
LIGHTMAP_SHADER = ROOT / "assets/minecraft/shaders/core/lightmap.fsh"
LEGACY_LIGHTMAP_SHADER = ROOT / "variants/legacy/assets/minecraft/shaders/core/lightmap.fsh"
GENERAL_SHADER = ROOT / "assets/flirty_beta/shaders/include/general.glsl"
INCLUDE = re.compile(r"#(?:include|moj_import) <flirty_beta:general.glsl>")


def read_text(path):
    return path.read_text(encoding="utf-8")


def compact(text):
    return re.sub(r"\s+", " ", text).strip()


class ResourcePackTests(unittest.TestCase):
    def test_required_pack_files_exist(self):
        for path in (PACK_META, ROOT / "pack.png", ROOT / "LICENSE", LIGHTMAP_SHADER, LEGACY_LIGHTMAP_SHADER, GENERAL_SHADER):
            with self.subTest(path=path.name):
                self.assertTrue(path.is_file())

    def test_build_ships_license(self):
        build_script = read_text(ROOT / "build.sh")

        self.assertIn('cp "${repo_dir}/LICENSE" "${staging_dir}/LICENSE"', build_script)
        self.assertEqual(build_script.count("pack.mcmeta pack.png LICENSE assets"), 2)

    def test_build_names_the_fork(self):
        build_script = read_text(ROOT / "build.sh")

        # the zip name is the title shown in the resource pack list
        self.assertIn('pack_name="Flirty Beta Fork"', build_script)
        self.assertEqual(build_script.count('"description": "Flirty Beta Fork (${version})"'), 2)

    def test_pack_metadata_matches_current_pack(self):
        metadata = json.loads(read_text(PACK_META))

        self.assertEqual(metadata["pack"]["description"], "Flirty Beta Fork (26.3)")
        self.assertEqual(metadata["pack"]["min_format"], 97)
        self.assertEqual(metadata["pack"]["max_format"], 97)

    def test_lightmap_uses_26_3_include(self):
        shader = read_text(LIGHTMAP_SHADER)

        self.assertIn("#include <flirty_beta:general.glsl>", shader)
        self.assertNotIn("#moj_import", shader)
        self.assertIn("#moj_import <flirty_beta:general.glsl>", read_text(LEGACY_LIGHTMAP_SHADER))

    def test_lightmap_uses_explicit_interface_locations(self):
        shader = compact(read_text(LIGHTMAP_SHADER))

        self.assertIn("#extension GL_ARB_separate_shader_objects : require", shader)
        self.assertIn("layout(location = 0) in vec2 texCoord;", shader)
        self.assertIn("layout(location = 0) out vec4 fragColor;", shader)

    def test_lightmap_info_block_matches_vanilla_26_3(self):
        shader = compact(read_text(LIGHTMAP_SHADER))

        self.assertIn(
            compact(
                """
                layout(std140) uniform LightmapInfo {
                    float SkyFactor;
                    float BlockFactor;
                    float NightVisionFactor;
                    float DarknessScale;
                    float BossOverlayWorldDarkeningFactor;
                    float BrightnessFactor;
                    vec3 BlockLightTint;
                    vec3 SkyLightColor;
                    vec3 AmbientColor;
                    vec3 NightVisionColor;
                } lightmapInfo;
                """
            ),
            shader,
        )

    def test_stepped_sky_light_is_on(self):
        self.assertIn("#define STEPPED_SKY_LIGHT 1", read_text(LIGHTMAP_SHADER))

    def test_general_include_has_guard(self):
        shader = read_text(GENERAL_SHADER)

        self.assertTrue(shader.startswith("#ifndef FLIRTY_BETA_GENERAL_GLSL\n#define FLIRTY_BETA_GENERAL_GLSL\n"))
        self.assertTrue(shader.rstrip().endswith("#endif"))

    @unittest.skipUnless(shutil.which("glslc"), "glslc not installed")
    def test_shaders_compile(self):
        general = read_text(GENERAL_SHADER)

        for path in (LIGHTMAP_SHADER, LEGACY_LIGHTMAP_SHADER):
            with self.subTest(path=path.relative_to(ROOT)), tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp) / "lightmap.frag"
                source.write_text(INCLUDE.sub(lambda _: general, read_text(path)), encoding="utf-8")
                result = subprocess.run(
                    ["glslc", "-fshader-stage=frag", "--target-env=opengl", "-fauto-bind-uniforms",
                     "-fauto-map-locations", str(source), "-o", str(Path(tmp) / "lightmap.spv")],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
