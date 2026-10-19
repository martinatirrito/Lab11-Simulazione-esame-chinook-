from database.DB_connect import DBConnect
from model.arco import Arco
from model.artist import Artist


class DAO():
    @staticmethod
    def getAllGenre():
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)

        except ConnectionError:
            print("Errore di connessione al databse")
            return

        result = []

        query = """select distinct g.Name as genre 
                    from Genre g 
                    order by genre ASC 
                    """


        cursor.execute(query, )

        for row in cursor:
            result.append(row["genre"])

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllNodes(genre): #NODI SONO GLI ARTISTI CHE POSSEDIONO ALMENO UN TRACK APPARTENENTE AL GENERE SELEZIONATO
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)

        except ConnectionError:
            print("Errore di connessione al databse")
            return

        result = []

        query = """select distinct a.*
                    from Artist a, album al, Track t, Genre g 
                    where a.ArtistId = al.ArtistId and al.AlbumId = t.AlbumId and t.GenreId = g.GenreId 
                    and g.Name = %s """

        cursor.execute(query, (genre, ))

        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(genre, idMapA):  # ESISTE ARCO SE UN CLIENTE HA ACQUISTATO BRANI DI ENTRAMBI ARTISTI A E B
                        # ARCHI VERSO IN BASE ALLA POPOLARITA COME SOMMA DEI BRANI ACQUISTATI DELL'ARTISTA. PESO SOMMA POP
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)

        except ConnectionError:
            print("Errore di connessione al databse")
            return

        result = []

        query = """select distinct c1.ArtistId as a1, c2.ArtistId as a2, p1.popolarita + p2.popolarita as peso
                    from (select distinct i.CustomerId, a.ArtistId
                            from invoice i, InvoiceLine il, track t, album a, Artist ar, Genre g
                            WHERE i.InvoiceId = il.InvoiceId and il.TrackId = t.TrackId and t.AlbumId = a.AlbumId and a.ArtistId = ar.ArtistId and t.GenreId = g.GenreId
                            and g.Name = %s) c1,
                            (select distinct i.CustomerId, a.ArtistId
                                    from invoice i, InvoiceLine il, track t, album a, Artist ar, Genre g
                                    WHERE i.InvoiceId = il.InvoiceId and il.TrackId = t.TrackId and t.AlbumId = a.AlbumId and a.ArtistId = ar.ArtistId and t.GenreId = g.GenreId
                                    and g.Name = %s) c2,
                            (select a.ArtistId, SUM(il.Quantity) as popolarita
                                    from InvoiceLine il, track t, album a, Artist ar, Genre g
                                    WHERE il.TrackId = t.TrackId and t.AlbumId = a.AlbumId and a.ArtistId = ar.ArtistId and t.GenreId = g.GenreId
                                    and g.Name = %s
                                    group by a.ArtistId) p1,
                            (select a.ArtistId, SUM(il.Quantity) as popolarita
                                    from InvoiceLine il, track t, album a, Artist ar, Genre g
                                    WHERE il.TrackId = t.TrackId and t.AlbumId = a.AlbumId and a.ArtistId = ar.ArtistId and t.GenreId = g.GenreId
                                    and g.Name = %s
                                    group by a.ArtistId) p2				
                    where c1.CustomerId = c2.CustomerId and c1.ArtistId != c2.ArtistId
                    and c1.ArtistId = p1.ArtistId and c2.ArtistId = p2.ArtistId 
                    and p1.popolarita >= p2.popolarita """


        cursor.execute(query, (genre, genre, genre, genre))

        for row in cursor:
            result.append(Arco(idMapA[row["a1"]], idMapA[row["a2"]], row["peso"]))

        cursor.close()
        conn.close()
        return result