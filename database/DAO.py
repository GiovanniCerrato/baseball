from database.DB_connect import DBConnect
from model.team import Team


class DAO():
    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(t.`year`)
                    from teams t 
                    where t.`year`>= 1980
                    order by t.`year` asc """

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSquadreAnno(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.teamCode, t.name,t.`year`, sum(s.salary ) as salarioTotale
                    from salaries s, teams t, appearances a 
                    where s.`year` = t.`year` and t.`year` = a.`year` and a.`year` = %s
                    and t.ID = a.teamID and a.playerID = s.playerID
                    group by t.teamCode"""

        cursor.execute(query,(anno,))

        for row in cursor:

            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result


