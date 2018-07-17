import sqlite3
import config
from collections import defaultdict
import functools


class Logic():
    def get_db(self):
        db = sqlite3.connect(config.db_path)
        c = db.cursor()
        return db, c

    def get_table_editable(self):
        db, cursor = self.get_db()
        data = {}
        lines = []
        competitions = []
        teams = []

        line = [{"id": "none:0", "value": ""}]
        cursor.execute("SELECT id, name FROM competitions ORDER BY id")
        for comp in cursor.fetchall():
            line.append({"id": f"comp:{comp[0]}", "value": comp[1]})
        data["header"] = line

        cursor.execute("SELECT id, name FROM teams")
        for team in cursor.fetchall():
            teams.append((team[0], team[1]))

        data["scores"] = []
        for team in teams:
            line = [{"id": f"team:{team[0]}", "value": team[1]}]
            sum = 0
            for competition in data["header"]:
                comp_id = competition["id"].split(":")[1]
                if "none" in competition["id"]:
                    continue
                cursor.execute("SELECT id, points FROM results WHERE competition_id=? AND team_id=?",
                               (comp_id, team[0]))
                res = cursor.fetchone()
                if res is None:
                    line.append({"id": f"add:res:{team[0]}:{comp_id}", "value": "XXX"})
                else:
                    line.append({"id": f"res:{res[0]}", "value": self.points_to_str(res[1])})
                    sum += res[1]
            line.append({"id": f"sum:{team[0]}", "value": f"{self.points_to_str(sum)}"})

            data["scores"].append(line)

        data["header"].append({"id": "sums", "value": "Součet"})

        data["scores"].sort(key=lambda x: x[-1]["value"])
        print(data["scores"])

        return data

    def points_to_str(self, points):
        if points == int(points):
            return f"{points:.0f}"
        return f"{points:.1f}".replace(".", ",")

    def get_messages(self):
        db, cursor = self.get_db()
        cursor.execute("SELECT id, message FROM messages")
        messages = []
        for m in cursor.fetchall():
            messages.append({"id": f"msg:{m[0]}", "text": m[1]})
        return messages

    def process_edit(self, id, value):
        db, cursor = self.get_db()
        c = id.split(":")
        action = c[0]
        try:
            if action == "add":  # add new resukt/team/competition
                if c[1] == "res":  # add result
                    cursor.execute("INSERT INTO results  (team_id, competition_id, points) VALUES (?,?,?)",
                                   (c[2], c[3], float(value)))
                elif c[1] == "team":
                    print(value)
                    cursor.execute("INSERT INTO teams (name) VALUES (?)",
                                   [value])
                elif c[1] == "comp":
                    cursor.execute("INSERT INTO competitions (name) VALUES (?)",
                                   [value])
                elif c[1] == "msg":
                    cursor.execute("INSERT INTO messages (message) VALUES (?)",
                                   [value])

            elif action == "res":  # edit result
                print(c[1], value)
                cursor.execute("UPDATE results SET points = ? WHERE id = ?",
                               (float(value), c[1]))
            elif action == "team":  # edit team name
                cursor.execute("UPDATE teams SET name = ? WHERE id = ?",
                               (value, c[1]))
            elif action == "comp":  # edit copetition name
                cursor.execute("UPDATE competitions SET name = ? WHERE id = ?",
                               (value, c[1]))
            elif action == "msg":  # edit message
                cursor.execute("UPDATE messages SET message = ? WHERE id = ?",
                               (value, c[1]))
            elif action == "del":
                if c[1] == "res":
                    cursor.execute("DELETE FROM results WHERE id=?",
                                   [c[2]])
                elif c[1] == "team":
                    cursor.execute("DELETE FROM teams WHERE id=?",
                                   [c[2]])
                elif c[1] == "comp":
                    cursor.execute("DELETE FROM competitions WHERE id=?",
                                   [c[2]])
                elif c[1] == "msg":
                    cursor.execute("DELETE FROM messages WHERE id=?",
                                   [c[2]])
            db.commit()
            return "OK"
        except:
            return "NOK"


def sort_scores(a, b):
    print(a[-1]["value"] < b[-1]["value"])
    return a[-1]["value"] < b[-1]["value"]


[[{'id': 'team:6', 'value': 'Berserkové'}, {'id': 'res:16', 'value': '2'}, {'id': 'res:21', 'value': '2'},
  {'id': 'res:25', 'value': '3'}, {'id': 'sum:6', 'value': '7'}],
 [{'id': 'team:7', 'value': 'Ragnarok<br/>(Eyjafjallajökull)'}, {'id': 'res:17', 'value': '2'},
  {'id': 'res:20', 'value': '1'}, {'id': 'res:24', 'value': '2'}, {'id': 'sum:7', 'value': '5'}],
 [{'id': 'team:8', 'value': 'Arijové'}, {'id': 'res:18', 'value': '3'}, {'id': 'res:23', 'value': '4'},
  {'id': 'res:26', 'value': '4'}, {'id': 'sum:8', 'value': '11'}],
 [{'id': 'team:9', 'value': 'Skye'}, {'id': 'res:19', 'value': '4'}, {'id': 'res:22', 'value': '3'},
  {'id': 'res:27', 'value': '4'}, {'id': 'sum:9', 'value': '11'}]]
