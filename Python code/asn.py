import csv
import re
import requests
badASN={3223,3842,4250,4323,4694,5577,6724,6870,6939,7203,7489,7506,7850,7979,8075,8100,8455,8560,8972,9009,9370,10297,10439,10929,11588,11831,11878,12586,12876,12989,13213,13739,13926,14061,14127,14618,15003,15083,15395,15497,15510,15626,15734,16125,16262,16276,16284,16397,16509,16628,17216,18450,18779,18978,19318,19437,19531,19624,19844,19871,19969,20021,20264,20454,20473,20598,20738,20773,20836,20860,21100,21159,21321,21859,22363,22552,22781,23033,23342,23352,24482,24768,24875,24940,24961,24971,25163,25369,25379,25780,25820,27257,28753,29066,29073,29182,29302,29354,29465,29550,29691,29802,29838,29854,30083,30176,30475,30633,30693,30900,30998,31034,31103,32097,32181,32244,32475,32489,32613,32780,33070,33083,33182,33302,33330,33387,33438,33480,33724,33785,33891,34305,34971,34989,35017,35366,35415,35470,35662,35908,35916,36024,36114,36290,36351,36352,36666,36873,36887,36920,36970,37018,37088,37153,37170,37209,37230,37248,37269,37280,37308,37347,37377,37472,37506,37521,37540,37643,37661,37692,37714,38001,39020,39326,39351,39392,39572,40156,40244,40676,40824,40861,41653,41665,42160,42331,42473,42695,42708,42730,42831,43146,49505,43289,43317,43350,44050,44066,45102,45187,45470,45671,45815,46261,46430,46475,46562,46664,46805,46816,46844,47328,47447,47588,49349,49367,49453,49505,49532,49544,49981,50297,50613,50673,51159,51167,51191,51395,51430,51731,51765,51852,52048,52173,52219,53013,53340,53559,53597,53667,53755,53850,53889,54104,54203,54455,54489,54500,54540,55225,55286,55536,55933,55967,56322,56630,56934,57043,57169,57230,57858,58073,58305,59253,59349,59432,59504,59729,59764,60011,60068,60118,60404,60485,60505,60558,60567,60781,61102,61157,61317,61440,62217,62240,62282,62370,62471,62540,62567,63008,63018,63119,63128,63199,63473,63949,64245,64484,132816,133296,133480,133752,134451,136258,197155,197328,198310,199653,199883,200019,200039,201011,201525,202053,202836,203523,203629,204196,327705,327784,327813,327942,328035,394256,394330,394380,395089,395111,395978,20248,44901,200904,53057,200532,50968,135822,55293,57286,201200,24549,39458,200000,14576,54290,206898,60117,20448,201553,54825,31472,8556,29119,60476,25532,54500,49949,51698,42442,11274,57345,54817,200019,53342,33569,201983,132425,197395,42699,31698,42612,29311,54527,63213,27175,13209,29140,27223,31659,49834,49693,30152,19133,198414,45201,31981,62605,61280,53332,61147,51109,19234,40438,58797,26978,29748,35974,262990,43021,42695,39704,62899,53281,59103,59615,55761,52335,16973,196827,32647,14992,198968,196745,62071,132869,56106,32911,24931,57669,48896,45481,132509,39839,63129,53370,25048,28747,46433,55051,18570,13955,16535,22903,9823,46945,263032,36536,50986,199733,48825,35914,33552,52236,28855,198347,40728,18120,53914,12586,55720,27640,62563,202118,9290,45887,51050,20068,49485,40374,14415,46873,14384,54555,263237,20773,53918,4851,32306,133229,28216,36236,42210,51248,49815,34649,41562,33260,24220,52347,45486,33182,53055,51290,132225,133120,42776,55799,48446,263093,56732,42399,47385,40539,42244,29302,10929,47549,200147,393326,198171,57773,47583,43472,32338,9166,62082,198651,24725,29067,197902,42418,29097,196645,56110,23535,29869,62756,26484,25926,15189,20401,24679,25128,39756,32400,9412,9667,51294,23052,28099,45693,17881,17669,17918,50926,201634,22611,54641,61102,132071,10207,45577,132070,262603,29883,24558,38279,199997,50465,14120,11235,50655,17019,31240,199481,16862,47161,56784,59791,59677,202023,199990,50872,54839,58936,11230,62310,38894,47172,262287,46260,14442,133143,197648,39451,58922,27589,42400,133393,201597,28997,60800,33322,38001,199129,197372,57752,201670,14244,22152,34541,196678,43198,47625,42331,62049,35295,42311,53589,59705,36791,14160,34432,41062,59135,201630,25260,23108,40281,31590,10532,22720,27357,33070,45187,7595,26481,29713,13926,54203,62651,63128,62838,30849,14987,47577,54334,63916,50915,21217,59816,23273,59632,29452,59795,60739,15919,49313,57879,56617,62088,45179,27597,201702,32740,58667,12617,199847,25642,14567,35278,197914,41079,1442,43620,197439,198313,42705,44398,13909,34745,24958,17971,47143,59854,57682,3722,13647,20450,30235,47205,23881,198047,14986,17920,32275,50608,199213,262170,201862,43541,24381,10200,14708,27229,48093,42465,7598,30475,55229,7349,33251,52465,52270,45152,8477,198153,52925,61412,262978,53225,41427,53101,41369,35467,59554,52674,24611,48812,40715,201449,52321,29331,201709,53221,198432,51241,19969,56799,26277,58113,28333,42120,6718,20692,17439,132717,9925,132779,42622,6188,40819,24997,38107,36408,57363,46177,62026,61107,44725,4134,4837,14061,26347,14059,28006,17974,17451,23969,131090,9829,34588,50582,7713,7552,612,714,1442,2554,2635,2639,2818,3064,3170,3188,3210,3214,3223,3242,3396,3502,3563,3598,3700,3722,3791,3842,3900,3904,4250,4323,4583,4640,4694,4758,4785,4842,4851,5041,5048,5430,5517,5539,5541,5577,5602,5693,5755,5784,6134,6188,6218,6295,6364,6428,6560,6603,6659,6696,6718,6724,6729,6738,6870,6903,7040,7052,7156,7158,7203,7259,7289,7296,7309,7337,7349,7393,7455,7489,7496,7506,7514,7540,7544,7595,7598,7655,7678,7684,7753,7792,7819,7827,7850,7859,7880,7883,7907,7918,7979,8075,8095,8100,8219,8280,8304,8312,8315,8342,8455,8477,8495,8556,8560,8622,8685,8697,8739,8741,8875,8893,8903,8943,8972,9115,9123,9150,9166,9211,9268,9290,9308,9370,9371,9412,9597,9667,9683,9744,9802,9823,9833,9891,9925,9952,10105,10114,10122,10123,10200,10207,10229,10297,10439,10462,10532,10704,10732,10737,10741,10765,10843,10908,10929,10963,11029,11042,11051,11114,11230,11235,11274,11282,11320,11357,11555,11572,11588,11608,11734,11754,11831,11849,11854,11878,11931,11989,12179,12181,12182,12189,12200,12260,12337,12364,12488,12506,12555,12574,12586,12617,12637,12676,12679,12703,12720,12779,12824,12859,12876,12989,12993,13913,13209,13213,13238,13287,13332,13335,13354,13389,13414,13438,13445,13537,13557,13647,13649,13737,13739,13767,13768,13798,13886,13909,13911,13916,13926,13955,14029,14061,14116,14120,14127,14135,14141,14160,14179,14202,14230,14244,14280,14340,14361,14384,14415,14442,14567,14572,14576,14618,14670,14708,14745,14770,14782,14986,14987,14992,15003,15083,15085,15133,15148,15149,15169,15189,15216,15348,15388,15395,15401,15456,15497,15510,15598,15611,15626,15657,15685,15694,15699,15703,15734,15817,15826,15830,15919,15922,15954,15967,15987,16125,16247,16262,16276,16284,16312,16347,16371,16509,16535,16550,16556,16578,16625,16628,16862,16973,17018,17019,17048,17054,17139,17216,17312,17393,17408,17439,17440,17444,17470,17501,17514,17589,17669,17683,17819,17833,17881,17918,17920,17941,17971,17997,18013,18025,18120,18229,18254,18450,18501,18530,18570,18586,18645,18650,18779,18978,18981,18984,19084,19133,19148,19234,19237,19318,19324,19376,19437,19527,19529,19531,19551,19624,19679,19710,19816,19832,19842,19844,19871,19893,19894,19969,19994,20021,20068,20150,20161,20248,20264,20278,20326,20360,20401,20448,20450,20454,20473,20495,20546,20559,20598,20616,20621,20647,20649,20692,20714,20730,20738,20773,20836,20847,20853,20857,20860,20926,20940,21069,21100,21155,21159,21217,21260,21321,21350,21396,21409,21499,21501,21554,21584,21624,21679,21769,21777,21859,21887,21926,21983,22119,22152,22363,22418,22427,22458,22489,22552,22558,22606,22611,22612,22628,22652,22653,22676,22720,22769,22781,22822,22878,22893,22903,22915,22979,23005,23033,23052,23108,23273,23312,23338,23342,23352,23450,23470,23535,23537,23576,23650,23661,23686,23816,23824,23881,23884,24000,24009,24142,24186,24220,24282,24373,24381,24428,24429,24446,24466,24482,24541,24549,24558,24572,24611,24679,24725,24768,24785,24806,24875,24931,24940,24958,24961,24971,24973,24989,24994,24997,25048,25108,25128,25151,25163,25234,25260,25335,25369,25379,25459,25486,25504,25532,25542,25560,25577,25593,25642,25653,25697,25780,25820,25897,25926,26044,26045,26101,26272,26277,26337,26347,26481,26484,26496,26658,26753,26754,26930,26978,27175,27176,27223,27229,27257,27310,27323,27357,27382,27411,27524,27589,27597,27640,27715,27823,27846,28092,28099,28110,28216,28299,28333,28490,28639,28666,28747,28753,28824,28855,28878,28907,28924,28994,28997,29014,29017,29028,29045,29066,29067,29073,29097,29119,29132,29134,29140,29141,29169,29182,29222,29262,29278,29302,29311,29331,29354,29423,29452,29465,29486,29522,29550,29636,29686,29691,29713,29748,29789,29791,29802,29812,29838,29854,29869,29873,29883,29971,30083,30137,30152,30170,30176,30186,30235,30277,30279,30447,30475,30479,30496,30602,30633,30693,30781,30785,30811,30823,30827,30836,30849,30860,30870,30900,30938,30962,30968,30998,31034,31083,31103,31178,31229,31240,31244,31251,31400,31404,31463,31472,31477,31590,31624,31659,31698,31708,31715,31727,31797,31798,31807,31815,31863,31898,31981,32087,32097,32177,32181,32244,32275,32306,32311,32338,32400,32475,32489,32491,32579,32613,32647,32708,32714,32740,32748,32780,32781,32787,32875,32881,32911,32931,32934,32959,32986,32987,33028,33070,33083,33139,33182,33251,33260,33302,33322,33330,33333,33387,33438,33475,33480,33494,33517,33532,33552,33569,33611,33688,33724,33785,33876,33891,33968,33984,34011,34081,34088,34109,34119,34222,34224,34235,34240,34282,34300,34305,34309,34358,34360,34432,34541,34549,34619,34649,34665,34702,34738,34745,34762,34788,34895,34920,34931,34948,34971,34989,34991,35017,35041,35196,35278,35295,35297,35329,35366,35415,35425,35470,35540,35554,35555,35592,35662,35779,35908,35913,35914,35916,35974,36024,36114,36218,36236,36263,36290,36351,36352,36354,36408,36444,36454,36483,36489,36536,36542,36647,36666,36791,36873,36887,36920,36943,36970,37018,37088,37135,37153,37170,37209,37230,37248,37266,37268,37269,37280,37308,37347,37377,37472,37506,37518,37521,37540,37643,37661,37692,37714,37775,37907,37962,37963,38001,38107,38186,38197,38220,38226,38277,38279,38283,38364,38365,38478,38532,38631,38700,38719,38731,38735,38843,38880,38894,38913,38955,39020,39122,39227,39324,39326,39351,39368,39392,39451,39458,39523,39536,39566,39572,39647,39704,39729,39743,39756,39758,39782,39783,39790,39798,39839,39845,39923,39962,40021,40065,40092,40156,40165,40244,40281,40374,40395,40438,40446,40529,40539,40630,40665,40676,40715,40728,40775,40819,40824,40861,40975,41000,41011,41018,41062,41075,41079,41281,41331,41357,41369,41378,41390,41427,41500,41508,41535,41541,41562,41564,41628,41634,41653,41665,42018,42043,42093,42120,42152,42159,42160,42210,42220,42229,42244,42311,42331,42352,42399,42400,42418,42442,42457,42462,42465,42473,42503,42572,42602,42612,42622,42655,42694,42695,42699,42705,42708,42730,42776,42807,42831,42846,42861,42868,42910,42926,42964,42994,43021,43043,43072,43108,43146,43147,43198,43260,43289,43317,43350,43359,43362,43391,43444,43472,43541,43554,43620,43624,43641,43659,43711,43758,43773,43847,43927,43945,43962,44050,44066,44094,44112,44128,44133,44136,44204,44220,44227,44398,44414,44453,44476,44486,44520,44559,44684,44685,44709,44750,44812,44814,44853,44901,44922,44925,45012,45014,45017,45031,45052,45090,45102,45117,45146,45152,45179,45184,45187,45201,45235,45276,45328,45352,45382,45459,45470,45481,45486,45504,45538,45544,45569,45577,45629,45634,45638,45652,45671,45693,45731,45753,45815,45839,45887,45903,46015,46176,46177,46260,46261,46284,46293,46370,46430,46433,46475,46562,46573,46606,46636,46640,46664,46723,46805,46816,46841,46844,46873,46879,46931,46945,47002,47066,47142,47143,47161,47172,47196,47205,47215,47242,47328,47381,47385,47447,47500,47513,47521,47541,47544,47549,47577,47583,47588,47598,47602,47625,47692,47841,47860,47869,47886,47893,47920,47967,47995,48024,48028,48030,48066,48093,48095,48096,48252,48254,48266,48277,48282,48287,48324,48347,48348,48403,48434,48446,48492,48505,48551,48635,48684,48689,48716,48737,48812,48815,48823,48825,48854,48882,48896,48950,48974,49006,49063,49073,49074,49126,49173,49282,49302,49313,49349,49352,49367,49392,49434,49443,49447,49453,49467,49485,49505,49532,49544,49597,49604,49635,49643,49682,49693,49699,49815,49818,49834,49855,49879,49949,49964,49981,50056,50113,50131,50245,50297,50300,50340,50461,50465,50474,50500,50599,50608,50613,50630,50655,50673,50840,50867,50872,50891,50915,50926,50937,50939,50941,50957,50968,50986,51013,51050,51092,51109,51159,51167,51177,51191,51241,51248,51290,51294,51346,51395,51430,51445,51447,51468,51490,51557,51559,51659,51698,51718,51731,51747,51765,51790,51842,51852,51862,51961,51983,52000,52030,52048,52173,52219,52236,52270,52302,52321,52335,52347,52368,52393,52449,52465,52485,52499,52523,52674,52733,52925,53013,53055,53057,53101,53221,53225,53243,53281,53318,53332,53340,53342,53346,53356,53369,53370,53440,53559,53587,53589,53597,53611,53628,53648,53667,53723,53755,53812,53824,53850,53889,53914,53918,53974,54014,54046,54104,54113,54163,54203,54290,54334,54455,54456,54489,54500,54527,54540,54555,54561,54574,54600,54641,54643,54817,54825,54839,54994,54997,55000,55002,55017,55045,55051,55081,55106,55150,55225,55229,55256,55286,55293,55303,55359,55388,55470,55536,55639,55660,55688,55701,55720,55761,55799,55803,55805,55824,55832,55933,55967,55990,56067,56106,56110,56150,56268,56291,56309,56322,56430,56485,56577,56582,56611,56617,56630,56655,56694,56732,56740,56784,56799,56831,56851,56902,56934,57043,57054,57059,57129,57166,57168,57169,57172,57189,57230,57256,57286,57345,57363,57367,57433,57494,57497,57669,57682,57717,57724,57751,57752,57756,57773,57814,57844,57858,57878,57879,57880,57972,58003,58010,58014,58018,58061,58065,58073,58099,58110,58113,58212,58222,58262,58269,58305,58313,58366,58397,58404,58451,58487,58621,58667,58678,58683,58762,58765,58779,58791,58797,58827,58879,58922,58936,58940,58955,58962,58964,58969,59094,59135,59164,59210,59253,59344,59349,59371,59374,59384,59431,59432,59441,59447,59504,59545,59554,59615,59632,59677,59684,59705,59729,59749,59764,59791,59795,59796,59816,59854,59939,59943,59980,60011,60068,60071,60087,60117,60118,60144,60318,60330,60371,60372,60380,60394,60404,60422,60458,60460,60485,60505,60539,60558,60567,60610,60631,60695,60721,60739,60781,60798,60800,60819,60887,60937,60974,61047,61055,61098,61102,61107,61147,61157,61173,61211,61272,61280,61317,61323,61412,61422,61440,61493,61998,62000,62026,62049,62052,62058,62068,62071,62079,62080,62082,62088,62093,62115,62214,62217,62228,62240,62266,62282,62292,62294,62310,62355,62370,62416,62442,62468,62471,62485,62519,62540,62563,62567,62601,62605,62651,62703,62729,62741,62756,62785,62838,62874,62878,62899,62900,62904,62922,62927,63008,63018,63023,63043,63119,63128,63129,63157,63199,63213,63410,63473,63485,63695,63731,63759,63760,63761,63889,63916,63930,63940,63949,63956,63989,63990,63997,64013,64035,64050,64056,64067,64085,64236,64245,64425,64484,65075,80780,131149,131178,131321,131334,131353,131386,131392,131414,131423,131442,131447,131472,131775,131788,131921,131965,132056,132061,132070,132071,132111,132116,132198,132203,132212,132225,132231,132241,132322,132335,132425,132447,132453,132497,132509,132717,132721,132742,132757,132779,132813,132816,132825,132869,132883,132932,132976,132996,133001,133024,133115,133120,133143,133159,133199,133201,133222,133229,133296,133320,133393,133441,133480,133643,133676,133696,133720,133752,133775,133779,133800,133855,133997,134014,134022,134033,134190,134375,134426,134451,134548,134674,134837,134913,134926,134937,134963,135004,135026,135028,135031,135097,135161,135343,135357,135377,135402,135543,135555,135562,135581,135682,135706,135760,135822,135872,135917,135951,135967,136052,136146,136160,136170,136209,136258,136288,136374,136523,136557,136716,136800,136851,136899,136907,136933,136945,136950,136970,137166,137226,137434,137443,137517,137621,137951,137969,138152,138195,138245,138296,138538,138571,139021,139190,139265,139330,139341,139456,139640,139659,139805,140224,140227,140576,141159,141518,141995,142032,196645,196678,196713,196716,196745,196752,196827,197019,197043,197071,197145,197155,197216,197226,197286,197308,197328,197372,197395,197426,197439,197492,197540,197569,197648,197695,197712,197746,197812,197882,197902,197914,197922,198047,198066,198068,198153,198171,198203,198310,198313,198347,198414,198432,198605,198610,198651,198770,198785,198968,199129,199140,199176,199213,199246,199267,199274,199297,199429,199432,199481,199484,199524,199608,199610,199653,199716,199733,199758,199847,199874,199883,199990,199997,200000,200019,200039,200052,200062,200074,200079,200081,200083,200085,200107,200128,200137,200141,200147,200185,200313,200454,200484,200487,200494,200532,200548,200557,200617,200697,200698,200719,200775,200831,200859,200904,200960,201011,201106,201133,201200,201206,201233,201288,201292,201295,201351,201401,201446,201449,201499,201509,201525,201553,201597,201630,201634,201640,201670,201682,201702,201709,201813,201848,201862,201963,201983,201999,202023,202053,202054,202090,202118,202144,202171,202193,202242,202278,202302,202413,202422,202423,202425,202436,202469,202470,202505,202527,202533,202614,202661,202675,202678,202693,202699,202702,202726,202750,202769,202836,202958,202969,202984,203020,203025,203040,203044,203053,203059,203069,203120,203320,203405,203417,203418,203443,203459,203476,203523,203565,203576,203629,203631,203694,203706,203810,203950,203999,204085,204089,204105,204119,204139,204167,204185,204188,204196,204210,204213,204223,204293,204317,204333,204353,204472,204490,204601,204655,204815,204818,204872,204895,204957,204992,204997,205016,205072,205081,205124,205145,205220,205275,205422,205544,205565,205692,205770,205824,205835,205842,205848,205857,205869,205873,205884,205944,206005,206068,206087,206092,206102,206127,206170,206178,206206,206233,206246,206281,206352,206361,206469,206590,206592,206611,206644,206654,206728,206750,206751,206804,206892,206898,206977,206991,207027,207088,207096,207108,207125,207143,207155,207199,207200,207326,207333,207429,207459,207566,207636,207728,207786,207959,208161,208332,208476,208582,208626,208685,208846,209128,209150,209242,209378,209559,209574,209622,209623,209686,209711,209723,209735,209737,209813,209843,209853,209896,209946,210015,210079,210162,210239,210273,211341,211390,211642,211871,211895,212219,212238,212356,212811,212906,213035,213058,213122,213137,213192,213254,213322,213367,262170,262254,262256,262267,262287,262448,262603,262916,262954,262978,262990,263032,263093,263168,263179,263203,263237,263734,263735,263740,263744,263745,263812,263821,263829,264649,265831,265839,266855,269853,327697,327705,327784,327790,327813,327942,327979,328035,328095,328110,328170,328200,328286,328364,328543,328608,393326,393398,393504,393646,393715,393886,393927,393956,393960,394021,394056,394143,394194,394256,394277,394281,394303,394330,394380,394625,394695,394727,394996,395089,395092,395105,395111,395358,395532,395561,395681,395776,395886,395954,395978,396073,396190,396356,396362,396412,396507,396982,396989,397373,397384,397423,397539,397563,398101,398108,398110,398217,398271,398478,398779,398823,398968,398993,399626,399674,
}
print(len(badASN))
allASN=[]
with open('csvfile.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        try:
            allASN.insert(int(row[0]),[row[1],row[2]] )
        except:
            print(row)

def getASNhtml(asn):
    url="https://bgp.potaroo.net/cgi-bin/as-report?as=AS@@&view=2.0"
    url=re.sub("@@",str(asn),url)
    print(url)
    page = requests.get(url)

    temp=page.text
    newtemp=""
    l=temp.split("\n")
    for x in l:
        if "iframe"  in x or "center" in x or "img src" in x:
            continue
        else:
            newtemp+=x+"\n"

    file1 = open("myfile.html","w")
    file1.write(newtemp)
getASNhtml(987)