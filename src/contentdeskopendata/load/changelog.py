import os
import requests

class ChangeLogMaker:
    def copyAllChangelogfromReproURL(self):
        self.createChangelog("https://raw.githubusercontent.com/TSO-AG/python-contentdesk-opendata/refs/heads/main/CHANGELOG-2.0.md", "CHANGELOG-2.0.md")
        self.createChangelog("https://raw.githubusercontent.com/TSO-AG/python-contentdesk-opendata/refs/heads/main/CHANGELOG-2.1.md", "CHANGELOG-2.1.md")

    def createChangelog(self, url, name):
        response = requests.get(url)
        response.raise_for_status()

        os.makedirs("docs", exist_ok=True)
        if name == "":
            name = "CHANGELOG.md"
        changelog_path = os.path.join("docs", name)
        with open(changelog_path, "wb") as f:
            f.write(response.content)