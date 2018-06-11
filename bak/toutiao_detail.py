#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import sys

from fake_useragent import UserAgent
from scrapy import Spider, Request

from toutiao.items import ToutiaoDetailItem

reload(sys)
sys.setrecursionlimit(15000)
sys.setdefaultencoding('utf-8')

"""
请求参数配置
"""
req_fake_ua = UserAgent()
req_timeout = 10
req_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Connection': 'close',
    'Content-Type': 'application/json',
    'Referer': 'www.toutiao.com'
}


def get_req_header():
    """
    获取请求header
    :return:
    """
    req_header['User-Agent'] = str(req_fake_ua.random)
    return req_header


class ToutiaoDetailSpider(Spider):
    name = 'toutiao_detail'
    allowed_domains = ['toutiao.com']

    def start_requests(self):
        start_urls = ['http://toutiao.com/group/6531585724729262605/']
        # start_urls = ['http://toutiao.com/group/6531585724729262605/','http://toutiao.com/group/6546145534481007118/','http://toutiao.com/group/6537456710892651016/','http://toutiao.com/group/6534842057297494536/','http://toutiao.com/item/6449842603822153998/','http://toutiao.com/item/6467108681551970574/','http://toutiao.com/group/6546073167176139278/','http://toutiao.com/group/6556365890458223117/','http://toutiao.com/group/6554239331291103758/','http://toutiao.com/group/6547620891021279752/','http://toutiao.com/item/6454001530524664077/','http://toutiao.com/group/6546826178211086856/','http://toutiao.com/group/6549006519952736782/','http://toutiao.com/group/6557408671087723016/','http://toutiao.com/item/6436264653650657538/','http://toutiao.com/group/6552660037074944516/','http://toutiao.com/group/6552582336586711566/','http://toutiao.com/group/6535596261645484551/','http://toutiao.com/group/6520483717155127815/','http://toutiao.com/group/6527032511720063501/','http://toutiao.com/group/6530913826034942468/','http://toutiao.com/group/6559396034370339335/','http://toutiao.com/group/6547645177350062599/','http://toutiao.com/group/6559020594334007815/','http://toutiao.com/group/6530594285295763981/','http://toutiao.com/group/6518678443054334477/','http://toutiao.com/group/6545697418900406798/','http://toutiao.com/group/6554162327250272772/','http://toutiao.com/group/6551602929101439502/','http://toutiao.com/group/6549435380360282627/','http://toutiao.com/group/6537452032356254212/','http://toutiao.com/group/6549491085670875655/','http://toutiao.com/group/6558200866979971598/','http://toutiao.com/group/6547474486009004552/','http://toutiao.com/group/6552469751396827651/','http://toutiao.com/group/6548645746411831821/','http://toutiao.com/item/6463408595722567949/','http://toutiao.com/group/6557960637043966468/','http://toutiao.com/group/6556378880830079496/','http://toutiao.com/group/6556557819527561732/','http://toutiao.com/group/6550878238174872077/','http://toutiao.com/item/6470560921545605389/','http://toutiao.com/group/6551560798408278536/','http://toutiao.com/group/6558060136408023566/','http://toutiao.com/item/6462557863494549774/','http://toutiao.com/item/6465847585180483854/','http://toutiao.com/group/6553079491734798862/','http://toutiao.com/group/6551615215723610631/','http://toutiao.com/group/6548298193837228548/','http://toutiao.com/group/6547834253277659655/','http://toutiao.com/item/6434397710433911042/','http://toutiao.com/group/6554674295887364615/','http://toutiao.com/item/6467874450082627854/','http://toutiao.com/group/6548305417812836871/','http://toutiao.com/group/6551179354330628616/','http://toutiao.com/group/6551162648833032708/','http://toutiao.com/group/6548703107520397837/','http://toutiao.com/group/6533450786611921421/','http://toutiao.com/group/6555732524679561741/','http://toutiao.com/group/6529722485024244238/','http://toutiao.com/group/6558155939738812935/','http://toutiao.com/group/6549622309169136132/','http://toutiao.com/group/6547240206993457678/','http://toutiao.com/group/6550065689271468552/','http://toutiao.com/group/6551371192165466628/','http://toutiao.com/group/6559658176440959496/','http://toutiao.com/group/6532367233488781828/','http://toutiao.com/group/6551651541630059022/','http://toutiao.com/group/6548577127636140551/','http://toutiao.com/group/6550171942630982152/','http://toutiao.com/group/6557665791964086787/','http://toutiao.com/group/6547285238660203016/','http://toutiao.com/group/6560468831930679812/','http://toutiao.com/group/6546345127692993027/','http://toutiao.com/group/6551647548967223815/','http://toutiao.com/group/6554876875020173832/','http://toutiao.com/group/6552339228196340238/','http://toutiao.com/group/6510526585060196867/','http://toutiao.com/group/6547448336327115268/','http://toutiao.com/group/6545783662326055428/','http://toutiao.com/group/6517130544977805837/','http://toutiao.com/group/6556676348792799752/','http://toutiao.com/group/6525351328137347597/','http://toutiao.com/group/6553029315187966472/','http://toutiao.com/group/6551625216248775172/','http://toutiao.com/item/6441039285322776845/','http://toutiao.com/group/6550464700147040776/','http://toutiao.com/group/6545965155002352132/','http://toutiao.com/group/6547842520213094915/','http://toutiao.com/group/6550559813619679758/','http://toutiao.com/group/6560100025001574920/','http://toutiao.com/group/6554684921984582157/','http://toutiao.com/group/6554616047511536141/','http://toutiao.com/item/6428340180523942146/','http://toutiao.com/item/6442516619846484238/','http://toutiao.com/item/6467814657074659597/','http://toutiao.com/group/6546418455682220552/','http://toutiao.com/group/6546884915957334536/','http://toutiao.com/group/6554998211390472718/','http://toutiao.com/group/6540088780513083918/','http://toutiao.com/item/6467785783045521678/','http://toutiao.com/group/6530972361976447496/','http://toutiao.com/group/6526871996834251271/','http://toutiao.com/group/6554115864843518467/','http://toutiao.com/group/6542018201146884616/','http://toutiao.com/group/6554578154055270925/','http://toutiao.com/group/6547527586178662925/','http://toutiao.com/group/6557472597271904776/','http://toutiao.com/group/6545708786596708868/','http://toutiao.com/group/6550817432137630216/','http://toutiao.com/group/6530141556941259268/','http://toutiao.com/group/6558789222071796228/','http://toutiao.com/group/6558793807918268932/','http://toutiao.com/group/6551224654390886925/','http://toutiao.com/group/6556112181543305742/','http://toutiao.com/group/6550897215911494158/','http://toutiao.com/group/6555809236192854536/','http://toutiao.com/group/6560252940827755012/','http://toutiao.com/item/6447257037792346382/','http://toutiao.com/group/6549038569715925512/','http://toutiao.com/group/6557969901301006861/','http://toutiao.com/item/6538338300342567428/','http://toutiao.com/group/6527439545246417416/','http://toutiao.com/group/6548313041337844227/','http://toutiao.com/group/6552279724008145411/','http://toutiao.com/group/6549490817298334212/','http://toutiao.com/group/6546340660700512782/','http://toutiao.com/group/6560273357395198472/','http://toutiao.com/group/6557870351194259972/','http://toutiao.com/group/6530020054145171975/','http://toutiao.com/group/6547873525821080068/','http://toutiao.com/group/6550539482175635981/','http://toutiao.com/group/6537186657379025421/','http://toutiao.com/item/6474743172869128461/','http://toutiao.com/group/6550817897080422915/','http://toutiao.com/item/6457400944710648077/','http://toutiao.com/group/6549008083144671747/','http://toutiao.com/item/6464801314575483149/','http://toutiao.com/item/6462563860258750734/','http://toutiao.com/group/6546897041497260557/','http://toutiao.com/group/6545068682500899336/','http://toutiao.com/group/6551213067995185677/','http://toutiao.com/group/6555030859810865677/','http://toutiao.com/group/6547443065873760775/','http://toutiao.com/item/6468132006864617742/','http://toutiao.com/group/6540540521901720067/','http://toutiao.com/group/6547856408572854798/','http://toutiao.com/item/6473672052254441742/','http://toutiao.com/item/6439657542174900494/','http://toutiao.com/group/6553559783494910477/','http://toutiao.com/group/6532643338187702787/','http://toutiao.com/group/6555968502304342541/','http://toutiao.com/group/6559348565393539598/','http://toutiao.com/item/6468462233012666637/','http://toutiao.com/group/6537593422490894851/','http://toutiao.com/group/6550575685268668942/','http://toutiao.com/group/6546469036429935118/','http://toutiao.com/item/6460248436884111629/','http://toutiao.com/group/6556530544866230788/','http://toutiao.com/group/6558669641147744776/','http://toutiao.com/group/6547562655563907592/','http://toutiao.com/group/6552745874844287496/','http://toutiao.com/group/6558233910566715907/','http://toutiao.com/group/6559424821975843332/','http://toutiao.com/group/6526781882070204942/','http://toutiao.com/group/6557930418279023112/','http://toutiao.com/group/6556081614793736717/','http://toutiao.com/item/6450059026200789261/','http://toutiao.com/group/6550168714929504781/','http://toutiao.com/group/6558011973756256772/','http://toutiao.com/item/6464934569161261325/','http://toutiao.com/group/6547519913655796231/','http://toutiao.com/item/6467317768873050382/','http://toutiao.com/group/6542420731316142599/','http://toutiao.com/item/6435713743920824577/','http://toutiao.com/group/6549818189662913037/','http://toutiao.com/group/6539470552187273741/','http://toutiao.com/item/6428696245618868482/','http://toutiao.com/group/6556816434062688775/','http://toutiao.com/group/6546849310422598157/','http://toutiao.com/group/6556478277735678467/','http://toutiao.com/group/6533916563689439757/','http://toutiao.com/group/6551529246416699912/','http://toutiao.com/group/6547511270898139656/','http://toutiao.com/group/6553397040057942531/','http://toutiao.com/group/6535958079819743751/','http://toutiao.com/item/6475650681842696461/','http://toutiao.com/group/6558675914626957831/','http://toutiao.com/group/6552319011323904526/','http://toutiao.com/group/6551657353194766856/','http://toutiao.com/group/6529685794645344781/','http://toutiao.com/group/6553081026032173571/','http://toutiao.com/item/6463326116932223245/','http://toutiao.com/item/6462848748513919245/','http://toutiao.com/group/6545594410069918211/','http://toutiao.com/item/6426641874747916546/','http://toutiao.com/group/6547557429381431811/','http://toutiao.com/group/6547954055723876867/','http://toutiao.com/group/6548750023121699336/','http://toutiao.com/item/6468869681200496910/','http://toutiao.com/group/6550958252794839560/','http://toutiao.com/group/6557840432108143107/','http://toutiao.com/group/6547142428015460877/','http://toutiao.com/group/6551663991809114631/','http://toutiao.com/group/6558244147080200707/','http://toutiao.com/group/6541899038407524878/','http://toutiao.com/group/6553900014949630477/','http://toutiao.com/item/6446880379889516813/','http://toutiao.com/group/6554613961369584132/','http://toutiao.com/group/6557255822110360071/','http://toutiao.com/item/6522365816619401731/','http://toutiao.com/group/6553856588111675911/','http://toutiao.com/group/6559475716201644548/','http://toutiao.com/group/6556160992793854471/','http://toutiao.com/group/6518340513328792071/','http://toutiao.com/group/6551604696082022916/','http://toutiao.com/item/6426267355227095297/','http://toutiao.com/group/6547979292666495492/','http://toutiao.com/group/6549050077418095111/','http://toutiao.com/item/6443617644112249102/','http://toutiao.com/group/6554187767125901838/','http://toutiao.com/group/6556003912690696712/','http://toutiao.com/group/6556092877326254605/','http://toutiao.com/group/6551247598299120135/','http://toutiao.com/group/6548655205888557571/','http://toutiao.com/item/6471530472097710350/','http://toutiao.com/group/6529113999332606472/','http://toutiao.com/group/6559053291014062596/','http://toutiao.com/group/6519326401307345421/','http://toutiao.com/item/6468799627498881293/','http://toutiao.com/group/6549375416472175108/','http://toutiao.com/group/6546759942244663812/','http://toutiao.com/group/6558340835711123972/','http://toutiao.com/group/6542201322152657416/','http://toutiao.com/group/6552783837049389572/','http://toutiao.com/group/6545976716118983175/','http://toutiao.com/group/6553929739839472135/','http://toutiao.com/group/6556122778909540872/','http://toutiao.com/item/6467420489194144014/','http://toutiao.com/group/6553746183125205518/','http://toutiao.com/group/6524832509971137037/','http://toutiao.com/item/6468067065096831246/','http://toutiao.com/group/6550806101288288772/','http://toutiao.com/group/6553021692799615501/','http://toutiao.com/group/6550897050806911495/','http://toutiao.com/item/6453316333223280910/','http://toutiao.com/group/6543174620814508547/','http://toutiao.com/group/6551618768991158797/','http://toutiao.com/group/6547067953077027332/','http://toutiao.com/group/6558582049018479108/','http://toutiao.com/group/6526795201917223432/','http://toutiao.com/item/6472976134182011149/','http://toutiao.com/group/6555756882424758797/','http://toutiao.com/group/6522051858133942798/','http://toutiao.com/group/6549011255405838851/','http://toutiao.com/group/6551530361199788557/','http://toutiao.com/group/6556819389784523272/','http://toutiao.com/item/6464720556443828494/','http://toutiao.com/group/6556367592339014147/','http://toutiao.com/item/6436630200410177793/','http://toutiao.com/item/6444903933662986510/','http://toutiao.com/group/6550608718113800707/','http://toutiao.com/group/6548276914505646606/','http://toutiao.com/group/6554155330350088707/','http://toutiao.com/group/6548283783383089667/','http://toutiao.com/group/6518122638299103747/','http://toutiao.com/group/6544852554314940941/','http://toutiao.com/group/6545966650900873742/','http://toutiao.com/group/6556158831053767175/','http://toutiao.com/group/6559021116080259592/','http://toutiao.com/item/6465555986093441293/','http://toutiao.com/group/6527870850496987655/','http://toutiao.com/item/6440784720451076365/','http://toutiao.com/group/6536164309972550152/','http://toutiao.com/group/6545621774338359816/','http://toutiao.com/group/6560229058246869508/','http://toutiao.com/group/6557660789207990792/','http://toutiao.com/group/6528267150270923278/','http://toutiao.com/group/6553506564068606477/','http://toutiao.com/group/6560137536499352067/','http://toutiao.com/group/6534125745877287432/','http://toutiao.com/item/6426921355437932802/','http://toutiao.com/group/6553796387186672142/','http://toutiao.com/group/6547907186264113678/','http://toutiao.com/item/6468065741630341390/','http://toutiao.com/group/6540017555338166787/','http://toutiao.com/group/6545982885059363336/','http://toutiao.com/group/6554631440380723726/','http://toutiao.com/group/6553861403747287565/','http://toutiao.com/group/6532781493050147331/','http://toutiao.com/group/6548942599028212238/','http://toutiao.com/item/6468175071113380109/','http://toutiao.com/item/6449561819563426061/','http://toutiao.com/group/6558760942312620558/','http://toutiao.com/item/6447264830419108110/','http://toutiao.com/group/6547513981865558542/','http://toutiao.com/group/6551554975229542916/','http://toutiao.com/group/6533101027413983748/','http://toutiao.com/group/6551550791717487112/','http://toutiao.com/group/6550902715818443268/','http://toutiao.com/group/6532056010553557508/','http://toutiao.com/group/6549149203778503171/','http://toutiao.com/group/6559690124475499021/','http://toutiao.com/group/6555062077810016782/','http://toutiao.com/group/6546022446862959118/','http://toutiao.com/group/6553429253780668942/','http://toutiao.com/item/6461764300716376334/','http://toutiao.com/group/6558235827510444552/','http://toutiao.com/group/6553847235635839501/','http://toutiao.com/item/6444631183736176909/','http://toutiao.com/group/6558205232164110851/','http://toutiao.com/group/6553032055976886791/','http://toutiao.com/group/6554707795810189837/','http://toutiao.com/group/6556367281520116238/','http://toutiao.com/group/6554910010533478919/','http://toutiao.com/group/6545229701848236551/','http://toutiao.com/item/6439573352725086477/','http://toutiao.com/group/6554694758130778638/','http://toutiao.com/group/6533543885224804868/','http://toutiao.com/group/6544881805701415428/','http://toutiao.com/group/6548313747516031501/','http://toutiao.com/group/6547475415974281735/','http://toutiao.com/group/6530457349528748547/','http://toutiao.com/group/6558974165691400708/','http://toutiao.com/group/6550641624651661831/','http://toutiao.com/group/6548728670737924622/','http://toutiao.com/item/6431125378021982465/','http://toutiao.com/item/6423566028097192194/','http://toutiao.com/item/6468584879629009166/','http://toutiao.com/group/6526138746956415502/','http://toutiao.com/item/6444638559021302030/','http://toutiao.com/item/6469622430821253390/','http://toutiao.com/item/6451158577955471630/','http://toutiao.com/item/6456723686136217869/','http://toutiao.com/group/6555459879396442637/','http://toutiao.com/item/6468045825191706893/','http://toutiao.com/group/6546189089182319111/','http://toutiao.com/group/6538928152255660557/','http://toutiao.com/group/6545297971297124878/','http://toutiao.com/group/6534534371754377731/','http://toutiao.com/group/6523045561237504516/','http://toutiao.com/group/6557002846171038221/','http://toutiao.com/item/6460338330025328910/','http://toutiao.com/group/6540475538861982215/','http://toutiao.com/group/6559019067854815757/','http://toutiao.com/group/6548739189943304717/','http://toutiao.com/group/6548223621070848515/','http://toutiao.com/group/6556489299003441672/','http://toutiao.com/item/6437448623771877633/','http://toutiao.com/group/6552827857360388621/','http://toutiao.com/item/6474431936629571853/','http://toutiao.com/group/6537931711747981828/','http://toutiao.com/group/6529029126966215176/','http://toutiao.com/group/6555609838703870468/','http://toutiao.com/group/6557957833470509572/','http://toutiao.com/group/6560096579666051588/','http://toutiao.com/group/6547827679838601731/','http://toutiao.com/item/6454373835989844238/','http://toutiao.com/group/6556741360945201678/','http://toutiao.com/group/6553397840977068551/','http://toutiao.com/item/6455222410147791118/','http://toutiao.com/group/6553509032206795267/','http://toutiao.com/group/6551694830072758798/','http://toutiao.com/item/6474751647187730701/','http://toutiao.com/group/6549414155428823566/','http://toutiao.com/group/6544890764252414471/','http://toutiao.com/group/6527922896734519821/','http://toutiao.com/group/6551351242503750158/','http://toutiao.com/group/6537277309836067341/','http://toutiao.com/group/6555256357023384077/','http://toutiao.com/item/6441194097033085198/','http://toutiao.com/group/6549451506200871438/','http://toutiao.com/group/6549433552377741832/','http://toutiao.com/item/6467070037424341261/','http://toutiao.com/group/6558652966318899719/','http://toutiao.com/group/6551649080454414856/','http://toutiao.com/group/6519272984539038211/','http://toutiao.com/group/6560209271118627331/','http://toutiao.com/group/6551656265733374472/','http://toutiao.com/item/6451523317684764942/','http://toutiao.com/group/6557836989737992717/','http://toutiao.com/item/6475446397083582734/','http://toutiao.com/group/6538903967437423118/','http://toutiao.com/group/6552672401585340932/','http://toutiao.com/item/6463845007055913230/','http://toutiao.com/group/6549396838359761421/','http://toutiao.com/group/6554252858298991108/','http://toutiao.com/group/6548213172799537668/','http://toutiao.com/group/6549032995301360132/','http://toutiao.com/group/6544635377305518599/','http://toutiao.com/item/6464081963044045070/','http://toutiao.com/item/6434707483192721665/','http://toutiao.com/group/6559901548892127751/','http://toutiao.com/group/6547979399138902535/','http://toutiao.com/item/6446762163221561613/','http://toutiao.com/group/6545614336914620935/','http://toutiao.com/group/6559833783745380877/','http://toutiao.com/group/6542723363280781831/','http://toutiao.com/group/6519276047198847491/','http://toutiao.com/group/6559866112182321667/','http://toutiao.com/group/6553482723397206542/','http://toutiao.com/item/6466209684331168014/','http://toutiao.com/group/6548677604981867016/','http://toutiao.com/group/6526488885126496776/','http://toutiao.com/group/6552334997401895432/','http://toutiao.com/group/6548281404126396931/','http://toutiao.com/group/6532997678823899662/','http://toutiao.com/group/6559337121620951555/','http://toutiao.com/group/6548634780928311811/','http://toutiao.com/group/6555735283084558861/','http://toutiao.com/group/6555812751980102152/','http://toutiao.com/group/6559400595969540616/','http://toutiao.com/group/6546423479204315662/','http://toutiao.com/item/6469253627805434126/','http://toutiao.com/group/6560231949212844547/','http://toutiao.com/group/6542003194157859335/','http://toutiao.com/item/6447379191179510029/','http://toutiao.com/group/6536509261617299981/','http://toutiao.com/group/6530445757814669837/','http://toutiao.com/group/6555713727000216071/','http://toutiao.com/item/6449879760322429198/','http://toutiao.com/group/6548690177236140552/','http://toutiao.com/item/6426650712410685697/','http://toutiao.com/group/6554519429495915016/','http://toutiao.com/group/6547891482626359815/','http://toutiao.com/group/6557602763386126852/','http://toutiao.com/group/6551926611845841416/','http://toutiao.com/group/6547930624101974541/','http://toutiao.com/item/6438550272590479618/','http://toutiao.com/item/6448413173925019918/','http://toutiao.com/group/6519404215205364238/','http://toutiao.com/group/6546342909245915661/','http://toutiao.com/group/6551271599465562631/','http://toutiao.com/group/6556833709138379277/','http://toutiao.com/group/6528892030158897671/','http://toutiao.com/group/6555746395008008717/','http://toutiao.com/group/6549043562623795726/','http://toutiao.com/item/6447629268691190029/','http://toutiao.com/group/6558309416955806211/','http://toutiao.com/group/6529778976305447432/','http://toutiao.com/group/6530217486950859267/','http://toutiao.com/item/6444798560771768590/','http://toutiao.com/item/6458880904960934157/','http://toutiao.com/group/6528584958728995341/','http://toutiao.com/item/6451432044848218381/','http://toutiao.com/item/6474159120982212877/','http://toutiao.com/group/6547087721444147716/','http://toutiao.com/item/6466267987807568142/','http://toutiao.com/preview_article/?pgc_id=6516671096769479182','http://toutiao.com/item/6444462747680768269/','http://toutiao.com/item/6474104455733182734/','http://toutiao.com/group/6514427688470446605/','http://toutiao.com/item/6445397136140927245/','http://toutiao.com/group/6559748523825299981/','http://toutiao.com/item/6448891633294377229/','http://toutiao.com/group/6547911600643244552/','http://toutiao.com/group/6559811966758552067/','http://toutiao.com/group/6555740798720147971/','http://toutiao.com/item/6450618766479851789/','http://toutiao.com/group/6555334275363766791/','http://toutiao.com/group/6531900987697791492/','http://toutiao.com/group/6542629858193703438/','http://toutiao.com/group/6535331155061768718/','http://toutiao.com/item/6447284867758555405/','http://toutiao.com/item/6454070939012301070/','http://toutiao.com/group/6546399960085037576/','http://toutiao.com/group/6534865092750606856/','http://toutiao.com/item/6450711402381312270/','http://toutiao.com/group/6550403053479002637/','http://toutiao.com/item/6467297900102680845/','http://toutiao.com/group/6548649105315332622/','http://toutiao.com/group/6559739132925444612/','http://toutiao.com/group/6545581073126916612/','http://toutiao.com/group/6546124420107207175/','http://toutiao.com/group/6553145303170548237/','http://toutiao.com/group/6552771077162926606/','http://toutiao.com/group/6555718826078503432/','http://toutiao.com/group/6557582162302861832/','http://toutiao.com/item/6463269187899883790/','http://toutiao.com/item/6445771087568437517/','http://toutiao.com/group/6556815023094628878/','http://toutiao.com/item/6436297394052137218/','http://toutiao.com/group/6549388410241417731/','http://toutiao.com/item/6462642140890530061/','http://toutiao.com/item/6458393798736085261/','http://toutiao.com/group/6557475526636732931/','http://toutiao.com/group/6559438562763211277/','http://toutiao.com/group/6549437014758916612/','http://toutiao.com/group/6553418478043267598/','http://toutiao.com/group/6554154533600100878/','http://toutiao.com/item/6465816350064378125/','http://toutiao.com/item/6465643243034902797/','http://toutiao.com/group/6557237379529179652/','http://toutiao.com/group/6555689724781003271/','http://toutiao.com/group/6545697950968840718/','http://toutiao.com/item/6462501020197978382/','http://toutiao.com/item/6439206127669346573/','http://toutiao.com/item/6468252371360153870/','http://toutiao.com/group/6551162774787981827/','http://toutiao.com/item/6430810587080425729/','http://toutiao.com/group/6543334262026797581/','http://toutiao.com/item/6455866817553367310/','http://toutiao.com/group/6556750060393071107/','http://toutiao.com/group/6550796311883416077/','http://toutiao.com/group/6551237486817837582/','http://toutiao.com/group/6550240469505278477/','http://toutiao.com/group/6554902201511182862/','http://toutiao.com/item/6449699004325298446/','http://toutiao.com/group/6553888128585695752/','http://toutiao.com/group/6551221377959988494/','http://toutiao.com/group/6557935550114824711/','http://toutiao.com/group/6553971559541768712/','http://toutiao.com/group/6520575043427107332/','http://toutiao.com/group/6549434998074638852/','http://toutiao.com/group/6543875672287216141/','http://toutiao.com/group/6537618286555693571/','http://toutiao.com/item/6452868293362450702/','http://toutiao.com/group/6557457594795950600/','http://toutiao.com/group/6554657280745275907/','http://toutiao.com/group/6528673806775484931/','http://toutiao.com/group/6558274865332224525/','http://toutiao.com/group/6558201359370289672/','http://toutiao.com/group/6553128325508760077/']
        for start_url in start_urls:
            yield Request(url=start_url, headers=get_req_header(), callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        try:
            detail_html = response.body
            title = response.css('article-title')
            self.logger.info('title is {}'.format(title))
            # crawl_data_path = os.path.abspath('../../data_detail/') + time.strftime('%Y-%m-%d', datetime.datetime.now().timetuple())
            # if not os.path.exists(crawl_data_path):
            #     os.mkdir(crawl_data_path)
            # file_name = response.url
            # outfile = crawl_data_path + "/" + file_name
            # with open(outfile, "wb") as code:
            #     code.write(detail_html)
            item = ToutiaoDetailItem()
            item.content = detail_html
            self.logger.info('crawl toutiao detail finish: url is %s, outfile is %s' % (response.url, outfile))
            yield item
        except Exception as e:
            self.logger.exception('crawl toutiao detail has an error {}'.format(e))
