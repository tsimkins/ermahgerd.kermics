COMIC_SERIES = {
    'andycapp' : 'Andy Capp',
    'arlonjanis' : 'Arlo and Janis',
    'babyblues' : 'Baby Blues',
    'bbailey' : 'Beetle Bailey',
    'bbailey-vintage' : 'Beetle Bailey (Vintage)',
    'bc' : 'B.C.',
    'bignate' : 'Big Nate',
    'bignate-vintage' : 'Big Nate (Vintage)',
    'bizarro' : 'Bizarro',
    'blondie' : 'Blondie',
    'buckles' : 'Buckles',
    'chickweed' : 'Chickweed',
    'close' : 'Close to Home',
    'dilbert' : 'Dilbert',
    'dilbert-vintage' : 'Dilbert (Vintage)',
    'drabble' : 'Drabble',
    'forbetter' : 'For Better or For Worse',
    'foxtrot' : 'Foxtrot',
    'frazz' : 'Frazz',
    'garfield' : 'Garfield',
    'getfuzzy' : 'Get Fuzzy',
    'graffiti' : 'Graffiti',
    'hagar' : 'Hagar the Horrible',
    'hinlois' : 'Hi and Lois',
    'jumpstart' : 'Jumpstart',
    'lockhorns' : 'Lockhorns',
    'looseparts' : 'Loose Parts',
    'mfillmore' : 'Mallard Fillmore',
    'monty' : 'Monty',
    'mothergoose' : 'Mother Goose and Grimm',
    'mutts' : 'Mutts',
    'nonsequitur' : 'Nonsequitur',
    'officehours-vintage' : 'Office Hours (Vintage)',
    'pearls' : 'Pearls',
    'phantom' : 'Phantom',
    'phantomsunday' : 'Phantom (Sunday)',
    'phantom-vintage' : 'Phantom (Vintage)',
    'pricklycity' : 'Prickly City',
    'reallifeadventures' : 'Real Life Adventures',
    'roseisrose' : 'Rose is Rose',
    'shermanslagoon' : 'Sherman\'s Lagoon',
    'shoe' : 'Shoe',
    'speedbump' : 'Speed Bump',
    'wizardofid' : 'Wizard of Id',
    'zits' : 'Zits',
}

APP_ROOT = '/home/simkintr/python/projects/ermahgerd.kermics'

COMIC_FILES = """
/home/jpoirier/public_html/comics/20151003
/home/jpoirier/public_html/comics/20151005
/home/jpoirier/public_html/comics/20151008
/home/jpoirier/public_html/comics/20150927
/home/jpoirier/public_html/comics/20151002
/home/jpoirier/public_html/comics/20151006
/home/jpoirier/public_html/comics/20151007
/home/jpoirier/public_html/comics/20150929
/home/jpoirier/public_html/comics/20150928
/home/jpoirier/public_html/comics/20151001
/home/jpoirier/public_html/comics/20151004
/home/jpoirier/public_html/comics/20150930
/home/jpoirier/public_html/comics/20151010
/home/jpoirier/public_html/comics/20151009
""".strip().split()

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/db/kermics.db' % APP_ROOT
