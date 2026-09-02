from html.parser import HTMLParser
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "site" / "index.html"


class PortalParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.stylesheets = []
        self.canonicals = []
        self.scripts = []
        self.heading_levels = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and "href" in attributes:
            self.links.append(attributes["href"])
        if tag == "img":
            self.images.append(attributes)
        if tag == "link" and attributes.get("rel") == "stylesheet":
            self.stylesheets.append(attributes.get("href"))
        if tag == "link" and attributes.get("rel") == "canonical":
            self.canonicals.append(attributes.get("href"))
        if tag == "script" and "src" in attributes:
            self.scripts.append(attributes["src"])
        if tag in {"h1", "h2", "h3"}:
            self.heading_levels.append(int(tag[1]))


class PortalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = INDEX.read_text(encoding="utf-8")
        cls.parser = PortalParser()
        cls.parser.feed(cls.source)

    def test_confirmed_yanoa_destinations_are_present(self):
        expected = {
            "https://home.yanoa.be",
            "https://racing.yanoa.be",
            "https://astro.yanoa.be",
            "https://telemetry.yanoa.be",
            "https://dechapper.be",
            "https://zonhoven-united.be",
        }
        self.assertTrue(expected.issubset(set(self.parser.links)))

    def test_personal_identity_and_contact_are_primary_content(self):
        for text in (
            "Dirk Smeets",
            "Engineer",
            "Teacher",
            "Astrophotographer",
            "Radio Amateur - ON1DGN",
            "mailto:dirk.smeets@yanoa.be",
            "https://www.instagram.com/d1rksm33ts/",
            "https://www.astrobin.com/users/d1rksm33ts/",
            "https://www.qrz.com/db/ON1DGN",
        ):
            self.assertIn(text, self.source)

        self.assertNotIn("tel:", self.source)
        self.assertNotIn("Technologist", self.source)

        self.assertTrue((ROOT / "site" / "assets" / "dirk.jpg").is_file())
        stylesheet = (ROOT / "site" / "assets" / "site.css").read_text(
            encoding="utf-8"
        )
        self.assertIn('/assets/dirk.jpg', stylesheet)

    def test_apps_and_websites_are_separate(self):
        for text in (
            'id="apps-title">YaNoa Apps',
            'id="websites-title">Websites',
            "Home Portal",
            "YaNoAstro",
            "YaNoa Racing",
            "DeChapper",
            "Zonhoven-United",
        ):
            self.assertIn(text, self.source)

        self.assertNotIn("Open my Yanoa apps", self.source)

    def test_assets_are_local(self):
        self.assertEqual(self.parser.stylesheets, ["/assets/site.css?v=20260902-7"])
        for image in self.parser.images:
            self.assertTrue(image.get("src", "").startswith("/assets/"))
            self.assertIn("alt", image)

    def test_document_has_one_primary_heading(self):
        self.assertEqual(self.source.count("<h1"), 1)
        self.assertEqual(self.parser.heading_levels[0], 1)

    def test_animation_scripts_are_local(self):
        self.assertEqual(
            self.parser.scripts,
            ["/assets/typed-2.0.12.min.js", "/assets/site.js"],
        )
        script = (ROOT / "site" / "assets" / "site.js").read_text(encoding="utf-8")
        self.assertIn("typeSpeed: 100", script)
        self.assertIn("backSpeed: 50", script)
        self.assertIn("backDelay: 2000", script)
        self.assertIn('history.scrollRestoration = "manual"', script)

    def test_application_cards_use_visual_previews(self):
        stylesheet = (ROOT / "site" / "assets" / "site.css").read_text(
            encoding="utf-8"
        )
        self.assertTrue(
            (ROOT / "site" / "assets" / "yanoa-racing-hero.webp").is_file()
        )
        self.assertIn('/assets/yanoa-racing-hero.webp', stylesheet)
        for asset in (
            "astro-m51.webp",
            "dechapper-hero.webp",
            "zonhoven-united-hero.webp",
        ):
            self.assertTrue((ROOT / "site" / "assets" / asset).is_file())
            self.assertIn(f'/assets/{asset}', stylesheet)
        self.assertIn("aspect-ratio: 16 / 9", stylesheet)

    def test_search_metadata_identifies_dirk(self):
        self.assertEqual(self.parser.canonicals, ["https://yanoa.be/"])
        for text in (
            "Dirk Smeets (ON1DGN) · YaNoa Engineering",
            'name="robots" content="index, follow, max-image-preview:large"',
            'property="og:type" content="profile"',
            'property="og:url" content="https://yanoa.be/"',
            'name="twitter:card" content="summary_large_image"',
            'id="profile-title"',
            "Belgian engineer",
        ):
            self.assertIn(text, self.source)

    def test_profile_page_structured_data_is_valid(self):
        marker = '<script type="application/ld+json">'
        payload = self.source.split(marker, 1)[1].split("</script>", 1)[0]
        structured_data = json.loads(payload)

        self.assertEqual(structured_data["@type"], "ProfilePage")
        person = structured_data["mainEntity"]
        self.assertEqual(person["@type"], "Person")
        self.assertEqual(person["name"], "Dirk Smeets")
        self.assertEqual(person["alternateName"], "ON1DGN")
        self.assertIn("https://www.qrz.com/db/ON1DGN", person["sameAs"])

    def test_sitemap_and_robots_are_present(self):
        sitemap = (ROOT / "site" / "sitemap.xml").read_text(encoding="utf-8")
        robots = (ROOT / "site" / "robots.txt").read_text(encoding="utf-8")
        nginx = (ROOT / "nginx.conf").read_text(encoding="utf-8")

        self.assertIn("<loc>https://yanoa.be/</loc>", sitemap)
        self.assertIn("Sitemap: https://yanoa.be/sitemap.xml", robots)
        self.assertIn("try_files $uri $uri/ =404;", nginx)
        self.assertNotIn("try_files $uri $uri/ /index.html;", nginx)


if __name__ == "__main__":
    unittest.main()
