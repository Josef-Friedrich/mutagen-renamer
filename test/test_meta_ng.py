# -*- coding: utf-8 -*-

from audiorename.meta_ng import MetaNG as Meta
from audiorename.args import ArgsDefault
import unittest
import os


def get_meta(path_list):
    return Meta(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                *path_list), ArgsDefault())


class TestMeta(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta(['real-world', 'h', 'Hines_Earl',
                              'Just-Friends_1989', '06_Indian-Summer.mp3'])

    def test_artistsafe(self):
        self.assertEqual(self.meta.artistsafe, u'Earl Hines')

    def test_artistsafe_sort(self):
        self.assertEqual(self.meta.artistsafe_sort, u'Hines, Earl')

    def test_year_safe(self):
        self.assertEqual(self.meta.year_safe, '1989')

    def test_artist_initial(self):
        self.assertEqual(self.meta.artist_initial, u'h')

    def test_album_initial(self):
        self.assertEqual(self.meta.album_initial, u'j')


class TestArtistSafeUnit(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta(['files', 'album.mp3'])
        self.meta.albumartist_credit = u''
        self.meta.albumartist_sort = u''
        self.meta.albumartist = u''
        self.meta.artist_credit = u''
        self.meta.artist_sort = u''
        self.meta.artist = u''

    def assertArtistSort(self, key):
        setattr(self.meta, key, key)
        self.assertEqual(self.meta.artistsafe, key)
        self.assertEqual(self.meta.artistsafe_sort, key)

    def test_unkown(self):
        self.assertEqual(self.meta.artistsafe, u'Unknown')
        self.assertEqual(self.meta.artistsafe_sort, u'Unknown')

    def test_albumartist_credit(self):
        self.assertArtistSort('albumartist_credit')

    def test_albumartist_sort(self):
        self.assertArtistSort('albumartist_sort')

    def test_albumartist(self):
        self.assertArtistSort('albumartist')

    def test_artist_credit(self):
        self.assertArtistSort('artist_credit')

    def test_artist_sort(self):
        self.assertArtistSort('artist_sort')

    def test_artist(self):
        self.assertArtistSort('artist')

    def test_artist__artist_sort(self):
        self.meta.artist = 'artist'
        self.meta.artist_sort = 'artist_sort'
        self.assertEqual(self.meta.artistsafe, 'artist')
        self.assertEqual(self.meta.artistsafe_sort, 'artist_sort')

    def test_albumartist__artist__artist_sort(self):
        self.meta.albumartist = 'albumartist'
        self.meta.artist = 'artist'
        self.meta.artist_sort = 'artist_sort'
        self.assertEqual(self.meta.artistsafe, 'albumartist')
        self.assertEqual(self.meta.artistsafe_sort, 'artist_sort')

    def test_artist__albumartist_sort__artist_sort(self):
        self.meta.albumartist_sort = 'albumartist_sort'
        self.meta.artist = 'artist'
        self.meta.artist_sort = 'artist_sort'
        self.assertEqual(self.meta.artistsafe, 'artist')
        self.assertEqual(self.meta.artistsafe_sort, 'albumartist_sort')

    def test_shell_unfriendly(self):
        self.meta.args.shell_friendly = False
        self.meta.artist_sort = 'Lastname, Prename'
        self.assertEqual(self.meta.artistsafe_sort, 'Lastname, Prename')

    def test_shell_friendly(self):
        self.meta.args.shell_friendly = True
        self.meta.artist_sort = 'Lastname, Prename'
        self.assertEqual(self.meta.artistsafe_sort, 'Lastname_Prename')


class TestYearSafeUnit(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta(['files', 'album.mp3'])
        self.meta.year = None
        self.meta.original_year = None

    def test_empty(self):
        self.assertEqual(self.meta.year_safe, '')

    def test_year(self):
        self.meta.year = 1978
        self.assertEqual(self.meta.year_safe, '1978')

    def test_original_year(self):
        self.meta.original_year = 1978
        self.assertEqual(self.meta.year_safe, '1978')

    def test_year__original_year(self):
        self.meta.year = 2016
        self.meta.original_year = 1978
        self.assertEqual(self.meta.year_safe, '1978')


# class TestArtistSafe(unittest.TestCase):
#
#     def test_artist(self):
#         meta = get_meta('artist')
#         self.assertEqual(meta['artistsafe'], u'artist')
#
#     def test_artist_sort(self):
#         meta = get_meta('artist_sort')
#         self.assertEqual(meta['artistsafe_sort'], u'artist_sort')
#
#     def test_albumartist(self):
#         meta = get_meta('albumartist')
#         self.assertEqual(meta['artistsafe'], u'albumartist')


class TestDiskTrackUnit(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta(['files', 'album.mp3'])
        self.meta.track = u''
        self.meta.tracktotal = u''
        self.meta.disc = u''
        self.meta.disctotal = u''

    def test_empty(self):
        self.assertEqual(self.meta.disctrack, u'')

    def test_no_track(self):
        self.meta.disc = '2'
        self.meta.disctotal = '3'
        self.meta.tracktotal = '36'
        self.assertEqual(self.meta.disctrack, u'')

    def test_disc_track(self):
        self.meta.disc = '2'
        self.meta.track = '4'
        self.assertEqual(self.meta.disctrack, u'2-04')

    def test_disk_total_one(self):
        self.meta.disc = '1'
        self.meta.track = '4'
        self.meta.disctotal = '1'
        self.meta.tracktotal = '36'
        self.assertEqual(self.meta.disctrack, u'04')

    def test_all_set(self):
        self.meta.disc = '2'
        self.meta.track = '4'
        self.meta.disctotal = '3'
        self.meta.tracktotal = '36'
        self.assertEqual(self.meta.disctrack, u'2-04')

    def test_zfill_track(self):
        self.meta.track = '4'
        self.meta.tracktotal = '100'
        self.assertEqual(self.meta.disctrack, u'004')

        self.meta.tracktotal = '10'
        self.assertEqual(self.meta.disctrack, u'04')

        self.meta.tracktotal = '5'
        self.assertEqual(self.meta.disctrack, u'04')

    def test_zfill_disc(self):
        self.meta.track = '4'
        self.meta.tracktotal = '10'
        self.meta.disc = '2'
        self.meta.disctotal = '10'
        self.assertEqual(self.meta.disctrack, u'02-04')

        self.meta.disctotal = '100'
        self.assertEqual(self.meta.disctrack, u'002-04')


class TestDiskTrack(unittest.TestCase):

    def test_single_disc(self):
        meta = get_meta(['real-world', 'e', 'Everlast', 'Eat-At-Whiteys_2000',
                         '02_Black-Jesus.mp3'])
        self.assertEqual(meta.disctrack, u'02')

    def test_double_disk(self):
        meta = get_meta(['real-world', '_compilations', 't',
                         'The-Greatest-No1s-of-the-80s_1994',
                         '2-09_Respectable.mp3'])
        self.assertEqual(meta.disctrack, u'2-09')


class TestAlbumClean(unittest.TestCase):

    def setUp(self):
        self.meta = get_meta(['files', 'album.mp3'])

    def assertAlbumClean(self, album, compare=u'Lorem ipsum'):
        self.meta.album = album
        self.assertEqual(self.meta.album_clean, compare)

    def test_disc_removal(self):
        self.assertAlbumClean('Lorem ipsum (Disc 1)')
        self.assertAlbumClean('Lorem ipsum(Disc 1)')
        self.assertAlbumClean('Lorem ipsum (Disc)')
        self.assertAlbumClean('Lorem ipsum (Disk 100)')
        self.assertAlbumClean('Lorem ipsum (disk99)')

    def test_empty(self):
        self.assertAlbumClean('', '')

    def test_real_world(self):
        meta = get_meta(['real-world', '_compilations', 't',
                         'The-Greatest-No1s-of-the-80s_1994',
                         '2-09_Respectable.mp3'])
        self.assertEqual(meta.album_clean, u'The Greatest No.1s of the 80s')

#
# class TestWork(unittest.TestCase):
#
#     def test_work(self):
#         meta = get_classical([
#             'Mozart_Horn-concertos',
#             '01.mp3'
#         ])
#         self.assertEqual(
#             meta['work'],
#             u'Concerto for French Horn no. 1 in D major, ' +
#             u'K. 386b KV 412 I. Allegro'
#         )
#         self.assertEqual(
#             meta['mb_workid'],
#             u'21fe0bf0-a040-387c-a39d-369d53c251fe'
#         )
#         self.assertEqual(
#             meta['composer_sort'],
#             u'Mozart, Wolfgang Amadeus'
#         )
#
#
# class TestClassicalUnit(unittest.TestCase):
#
#     def setUp(self):
#         from audiorename import meta
#         self.meta = meta.Meta()
#
#     def test_classical_title(self):
#         self.assertEqual(self.meta.titleClassical('work: title'), 'title')
#         self.assertEqual(self.meta.titleClassical('work: work: title'),
#                          'work: title')
#         self.assertEqual(self.meta.titleClassical('title'), 'title')
#
#
# class TestClassical(unittest.TestCase):
#
#     def setUp(self):
#         self.mozart = get_classical([
#             'Mozart_Horn-concertos',
#             '01.mp3'
#         ])
#
#         self.mozart2 = get_classical([
#             'Mozart_Horn-concertos',
#             '02.mp3'
#         ])
#
#         self.schubert = get_classical([
#             'Schubert_Winterreise',
#             '01.mp3'
#         ])
#         self.tschaikowski = get_classical([
#             'Tschaikowski_Swan-Lake',
#             '1-01.mp3'
#         ])
#         self.wagner = get_classical([
#             'Wagner_Meistersinger',
#             '01.mp3'
#         ])
#
#     # album_classical
#     def test_album_classical_mozart(self):
#         self.assertEqual(
#             self.mozart['album_classical'],
#             u'Concerto for French Horn no. 1 in D major, K. 386b KV 412'
#         )
#
#     def test_album_classical_schubert(self):
#         self.assertEqual(
#             self.schubert['album_classical'],
#             u'Die Winterreise, op. 89, D. 911'
#         )
#
#     def test_album_classical_tschaikowski(self):
#         self.assertEqual(
#             self.tschaikowski['album_classical'],
#             u'Swan Lake, op. 20'
#         )
#
#     def test_album_classical_wagner(self):
#         self.assertEqual(
#             self.wagner['album_classical'],
#             u'Die Meistersinger von N\xfcrnberg'
#         )
#
#     # composer_initial
#     def test_composer_initial_mozart(self):
#         self.assertEqual(self.mozart['composer_initial'], u'm')
#
#     def test_composer_initial_schubert(self):
#         self.assertEqual(self.schubert['composer_initial'], u's')
#
#     def test_composer_initial_tschaikowski(self):
#         self.assertEqual(self.tschaikowski['composer_initial'], u't')
#
#     def test_composer_initial_wagner(self):
#         self.assertEqual(self.wagner['composer_initial'], u'w')
#
#     # composer_safe
#     def test_composer_safe_mozart(self):
#         self.assertEqual(
#             self.mozart['composer_safe'],
#             u'Mozart, Wolfgang Amadeus'
#         )
#
#     def test_composer_safe_mozart2(self):
#         self.assertEqual(
#             self.mozart2['composer_safe'],
#             u'Mozart, Wolfgang Amadeus'
#         )
#
#     def test_composer_safe_schubert(self):
#         self.assertEqual(
#             self.schubert['composer_safe'],
#             u'Schubert, Franz'
#         )
#
#     def test_composer_safe_tschaikowski(self):
#         self.assertEqual(
#             self.tschaikowski['composer_safe'],
#             u'Tchaikovsky, Pyotr Ilyich'
#         )
#
#     def test_composer_safe_wagner(self):
#         self.assertEqual(
#             self.wagner['composer_safe'],
#             u'Wagner, Richard'
#         )
#
#     # composer_sort
#     def test_composer_sort_mozart(self):
#         self.assertEqual(
#             self.mozart['composer_sort'],
#             u'Mozart, Wolfgang Amadeus'
#         )
#
#     def test_composer_sort_schubert(self):
#         self.assertEqual(
#             self.schubert['composer_sort'],
#             u'Schubert, Franz'
#         )
#
#     def test_composer_sort_tschaikowski(self):
#         self.assertEqual(
#             self.tschaikowski['composer_sort'],
#             u'Tchaikovsky, Pyotr Ilyich'
#         )
#
#     def test_composer_sort_wagner(self):
#         self.assertEqual(
#             self.wagner['composer_sort'],
#             u'Wagner, Richard'
#         )
#
#     # performer_classical
#     def test_performer_classical_mozart(self):
#         self.assertEqual(
#             self.mozart['performer_classical'],
#             u'OrpChaOrc'
#         )
#
#     def test_performer_classical_schubert(self):
#         self.assertEqual(
#             self.schubert['performer_classical'],
#             u'Fischer-Dieskau, Moore'
#         )
#
#     def test_performer_classical_tschaikowski(self):
#         self.assertEqual(
#             self.tschaikowski['performer_classical'],
#             u'Svetlanov, StaAcaSym'
#         )
#
#     def test_performer_classical_wagner(self):
#         self.assertEqual(
#             self.wagner['performer_classical'],
#             u'Karajan, StaDre, StaDre'
#         )
#
#     # title_classical
#     def test_title_classical_mozart(self):
#         self.assertEqual(self.mozart['title_classical'], u'I. Allegro')
#
#     def test_title_classical_schubert(self):
#         self.assertEqual(
#             self.schubert['title_classical'], u'Gute Nacht')
#
#     def test_title_classical_tschaikowski(self):
#         self.assertEqual(
#             self.tschaikowski['title_classical'],
#             u'Introduction. Moderato assai - Allegro, ma non troppo -
#               Tempo I'
#         )
#
#     def test_title_classical_wagner(self):
#         self.assertEqual(
#             self.wagner['title_classical'], u'Vorspiel')
#
#     # track_classical
#     def test_track_classical_mozart(self):
#         self.assertEqual(self.mozart['track_classical'], u'01')
#
#     def test_track_classical_schubert(self):
#         self.assertEqual(self.schubert['track_classical'], u'01')
#
#     def test_track_classical_tschaikowski(self):
#         self.assertEqual(self.tschaikowski['track_classical'], u'1-01')
#
#     def test_track_classical_wagner(self):
#         self.assertEqual(self.wagner['track_classical'], u'1-01')
#
#
# class TestTrackClassical(unittest.TestCase):
#
#     def setUp(self):
#         from audiorename import meta
#         self.meta = meta.Meta()
#
#     def assertRoman(self, roman, arabic):
#         self.assertEqual(roman_to_int(roman), arabic)
#
#     def test_roman_to_int(self):
#         self.assertRoman('I', 1)
#         self.assertRoman('II', 2)
#         self.assertRoman('III', 3)
#         self.assertRoman('IV', 4)
#         self.assertRoman('V', 5)
#         self.assertRoman('VI', 6)
#         self.assertRoman('VII', 7)
#         self.assertRoman('VIII', 8)
#         self.assertRoman('IX', 9)
#         self.assertRoman('X', 10)
#         self.assertRoman('XI', 11)
#         self.assertRoman('XII', 12)
#
#     def assertTrack(self, title, compare):
#         self.assertEqual(self.meta.trackClassical(title), compare)
#
#     def test_function(self):
#         self.assertTrack('III. Credo', u'03')
#         self.assertTrack('III Credo', '')
#         self.assertTrack('Credo', '')
#         self.assertEqual(self.meta.trackClassical('lol', 123), 123)
#
#
# class TestPerformer(unittest.TestCase):
#
#     def getMeta(self, extension):
#         return h.get_meta([h.dir_test, 'performers', 'blank.' + extension])
#
#     def assertPerformer(self, meta):
#         p = meta['performer_raw']
#         self.assertEqual(p[0][0], u'conductor')
#         self.assertEqual(p[0][1], u'Fabio Luisi')
#         self.assertEqual(p[1][0], u'orchestra')
#         self.assertEqual(p[1][1], u'Wiener Symphoniker')
#         self.assertEqual(p[2][0], u'soprano vocals')
#         self.assertEqual(p[2][1], u'Elena Filipova')
#         self.assertEqual(p[3][0], u'choir vocals')
#         self.assertEqual(p[3][1], u'Chor der Wiener Volksoper')
#
#         self.assertEqual(meta['performer'], u'Fabio Luisi, Wiener ' +
#                          u'Symphoniker, Elena Filipova, Chor der Wiener ' +
#                          u'Volksoper')
#         self.assertEqual(meta['performer_short'], u'Luisi, WieSym')
#
#     def test_unit_normalize_performer(self):
#         from audiorename import meta
#         meta = meta.Meta()
#         performer = [u'John Lennon (vocals)', u'Ringo Starr (drums)']
#         out = meta.normalizePerformer(performer)
#         self.assertEqual(out[0][0], u'vocals')
#         self.assertEqual(out[0][1], u'John Lennon')
#         self.assertEqual(out[1][0], u'drums')
#         self.assertEqual(out[1][1], u'Ringo Starr')
#
#     def test_unit_normalize_performer_string(self):
#         from audiorename import meta
#         meta = meta.Meta()
#         performer = u'Ludwig van Beethoven'
#         out = meta.normalizePerformer(performer)
#         self.assertEqual(out, [])
#
#     def test_flac(self):
#         meta = self.getMeta('ogg')
#         self.assertPerformer(meta)
#
#     def test_mp3(self):
#         meta = self.getMeta('mp3')
#         self.assertPerformer(meta)
#
#     def test_ogg(self):
#         meta = self.getMeta('ogg')
#         self.assertPerformer(meta)
#
#
# class TestPerformerUnit(unittest.TestCase):
#
#     def setUp(self):
#         self.performer = [[u'conductor', u'Lorin Mazel'],
#                           [
#                           u'orchestra',
#                           u'Orchester des Bayerischen Rundfunks'
#                           ],
#                           [u'choir vocals',
#                            u'Chor des Bayerischen Rundfunks'],
#                           [u'speaker', u'Loriot']]
#         from audiorename import meta
#         self.meta = meta.Meta()
#
#     def test_performer_short(self):
#         s = self.meta.performerShort(self.performer)
#         self.assertEqual(s, u'Mazel, OrcdesBay')
#
#     def test_performer_shorten(self):
#         s = self.meta.shortenPerformer(u'Ludwig van Beethoven')
#         self.assertEqual(s, u'Lud. van Bee.')
#
#     def test_performer_shorten_option_separator(self):
#         s = self.meta.shortenPerformer(u'Ludwig van Beethoven',
#                                        separator=u'--')
#         self.assertEqual(s, u'Lud.--van--Bee.')
#
#     def test_performer_shorten_option_abbreviation(self):
#         s = self.meta.shortenPerformer(u'Ludwig van Beethoven',
#                                        abbreviation=u'_')
#         self.assertEqual(s, u'Lud_ van Bee_')
#
#     def test_performer_shorten_option_all(self):
#         s = self.meta.shortenPerformer(u'Ludwig van Beethoven',
#                                        separator=u'',
#                                        abbreviation=u'')
#         self.assertEqual(s, u'LudvanBee')


class TestMetaNG(unittest.TestCase):

    def test_meta(self):
        meta = get_meta(['classical', 'Wagner_Meistersinger', '01.mp3'])

        self.assertEqual(meta.album_classical,
                         u'Die Meistersinger von Nürnberg')
        self.assertEqual(meta.album_clean,
                         u'Die Meistersinger von Nürnberg')
        self.assertEqual(meta.album_initial, u'd')
        self.assertEqual(
            meta.artistsafe,
            u'Richard Wagner; René Kollo, Helen Donath, Theo Adam, Geraint ' +
            'Evans, Peter Schreier, Ruth Hesse, Karl Ridderbusch, Chor der ' +
            'Staatsoper Dresden, MDR Rundfunkchor Leipzig, Staatskapelle ' +
            'Dresden, Herbert von Karajan')
        self.assertEqual(
            meta.artistsafe_sort,
            u'Wagner, Richard; Kollo, René, Donath, Helen, Adam, Theo, ' +
            'Evans, Geraint, Schreier, Peter, Hesse, Ruth, Ridderbusch, ' +
            'Karl, Chor der Staatsoper Dresden, MDR Rundfunkchor Leipzig, ' +
            'Staatskapelle Dresden, Karajan, Herbert von')
        self.assertEqual(meta.composer_safe, u'Wagner, Richard')
        self.assertEqual(meta.composer_initial, u'w')
        self.assertEqual(meta.disctrack, u'1-01')
        self.assertEqual(meta.title_classical, 'Vorspiel')


if __name__ == '__main__':
    unittest.main()