// 简体中文 —— 派对模式：「流星节」冒险与它的五个小游戏
// （src/party/story.js、src/party/games.js）。键就是英文原文。
// 霍利斯和各位主持人是对整队人说话；规则、手机提示和按钮是对每位玩家说话。
// 玩家性别未知，所以称号和对单人说的话都用中性词。
// 村民的闲聊气泡（CHATTER、HOLLIS_BITS）在 lines.js，地名与村民名在 ui.js / lines.js。
export const PARTY = {
  // ---------------------------------------------------------------- 冒险
  'The Starfall Festival': '流星节',
  'a Hearthlight party adventure': '一场炉火之光的朋友冒险',
  '{list} and {last}': '{list}和{last}',   // 「安娜、雷欧和萨姆」
  'friend': '朋友们',                        // 没人在场时用来代替名字

  // 开场（霍利斯）
  'Welcome, welcome! {names} — you made it for the Starfall Festival!': '欢迎，欢迎！{names}——你们赶上了流星节！',
  'Tonight the whole cove sends up the great Sky Lantern, so this year’s falling stars can find their way home.': '今晚整个海湾都会放飞巨大的天灯，好让今年的流星找到回家的路。',
  'But last night’s storm tore the five Star Charms right off it and flung them all over the valley!': '可是昨晚的暴风雨把五枚星之护符从灯上扯了下来，扔得满山谷都是！',
  'Our neighbours found every one — and they won’t hand them back without a little friendly challenge. It’s tradition.': '邻居们把它们全都找到了——不过想拿回来，得先过他们的小小友谊挑战。这是传统。',
  'Bring all five charms home before the stars fall. And do stick together… ish!': '在星星落下之前，把五枚护符都带回来。还有，大家要抱团……差不多吧！',

  // 选择去哪里（投票）
  'Where shall we look first?': '先去哪儿找？',
  '{n}/5 charms home! Where to next?': '已找齐 {n}/5 枚护符！接下来去哪儿？',
  'the Standing Stones': '立石阵',   // 投票标签
  // 目标（要短：手机上会接上「——跟着箭头走！」）
  'Find Bram at Honeydew Fields': '去蜜露田野找布拉姆',
  'Find Juniper at Frostpine Ridge': '去霜松岭找朱妮珀',
  'Find Ivy at Maple Hollow': '去枫林坳找艾薇',
  'Find Finn at Blossom Glade': '去繁花林找芬恩',
  'Find Mabel at the Standing Stones': '去立石阵找梅布尔',

  // 护符
  'Sun Charm': '太阳护符',
  'Frost Charm': '霜之护符',
  'Leaf Charm': '叶之护符',
  'Koi Charm': '锦鲤护符',
  'Star Charm': '星之护符',
  'Challenge complete!': '挑战完成！',
  'Time’s up!': '时间到！',
  '{charm} recovered!': '找回了{charm}！',
  '{n} of 5 Star Charms': '星之护符 {n}/5',

  // ---- 布拉姆 · 捉鸡大作战（蜜露田野）
  'Hen Round-Up': '捉鸡大作战',
  'Catch the hens, carry them to the coop': '抓住母鸡，抱回鸡舍',
  // 规则行必须能塞进规则卡的一行
  'The hens got out of the coop!': '母鸡们跑出鸡舍了！',
  '{a}: grab a hen · carry it to the coop': '{a}：抓住母鸡 · 抱回鸡舍',
  'A golden hen shows up halfway: worth 3!': '中途会出现金母鸡：值 3 分！',
  'Howdy, friends! The storm scared my hens clean out of the coop, and your Sun Charm is tangled up in all the fuss.': '嗨，朋友们！暴风雨把我的母鸡全吓出鸡舍了，你们的太阳护符也搅在这团乱里。',
  'Every last hen home! Here — the Sun Charm. It was in Buttercup’s water trough, of all places.': '最后一只母鸡也回家了！喏——太阳护符。它居然就在奶油花的水槽里。',

  // ---- 朱妮珀 · 雪球大乱斗（霜松岭）
  'Snowball Scramble': '雪球大乱斗',
  'Throw snowballs · jump to dodge': '扔雪球 · 跳跃闪避',
  'Snowball fight on the frozen pond!': '冻湖上的雪球大战！',
  '{a}: throw (it aims for you a little) · {b}: jump to dodge': '{a}：扔（会帮你瞄一点点）· {b}：跳起来闪避',
  'Hit friends or snowmen: +1 each. The ice is slippy!': '打中朋友或雪人：各 +1。冰面很滑！',
  'Oh hey, trail buddies! The Frost Charm froze into the pond — I chipped it out, but a ranger’s gotta have a little fun first…': '哦嘿，路上认识的朋友！霜之护符冻在池塘里了——我把它凿出来了，可巡林员总得先玩一小会儿……',
  'Ha! Best snowball fight the ridge has ever seen. The Frost Charm’s all yours!': '哈哈！这是霜松岭见过最棒的一场雪球大战。霜之护符归你们了！',

  // ---- 艾薇 · 橡果大搜寻（枫林坳）
  'Acorn Hunt': '橡果大搜寻',
  'Jump into leaf piles to find acorns': '跳进落叶堆里找橡果',
  'The squirrels hid their acorns in the leaf piles!': '松鼠把橡果藏进落叶堆了！',
  '{b}: jump INTO a pile to search it': '{b}：跳进落叶堆里翻找',
  'Acorns +1 · golden acorns +3 · piles grow back': '橡果 +1 · 金橡果 +3 · 落叶堆会重新堆好',
  'Hello hello! The wind blew the Leaf Charm into one of these piles… along with every acorn in the valley. Let’s dig!': '你好你好！风把叶之护符吹进了其中一堆里……连同整个山谷的橡果。开翻吧！',
  'Found it! Well, you found it — about forty acorns, and the Leaf Charm. The squirrels send their thanks.': '找到啦！好吧，是你们找到的——大约四十颗橡果，还有叶之护符。松鼠们向你们道谢。',

  // ---- 芬恩 · 钓锦鲤（繁花林）
  'Koi Catch': '钓锦鲤',
  'Cast, wait for the buzz, then press A!': '抛竿，等震动，然后按 A！',
  'A koi swallowed the Koi Charm (don’t worry, it spat it out).': '一条锦鲤吞了锦鲤护符（别担心，它吐出来了）。',
  '{a}: cast into the pond · wait for your phone to BUZZ': '{a}：抛进池塘 · 等你的手机震动',
  'Then {a}, quick! Golden koi +3 · the ancient koi +5': '然后快按 {a}！金锦鲤 +3 · 远古锦鲤 +5',
  'Oh — hi. So, uh, a koi swallowed the charm. It’s fine now. But Grandpa always said: first you fish, then you get the prize.': '哦——你好。那个，呃，一条锦鲤吞了护符。现在没事了。不过爷爷总说：先钓鱼，再拿奖。',
  'Not bad at all. Grandpa would’ve liked you lot. Here’s the Koi Charm.': '挺不错嘛。爷爷会喜欢你们这帮人的。锦鲤护符拿去吧。',

  // ---- 梅布尔 · 星石阵（立石阵）
  'Star Stones': '星石阵',
  'Everyone on a glowing star!': '所有人站上发光的星星！',
  'The old stones only open for friends who move as one.': '古老的石头只为同心同行的朋友打开。',
  'Every player stands on a glowing star at once (3 rounds)': '所有玩家同时站上发光的星星（3 轮）',
  'Then everybody JUMP together!': '然后所有人一起跳！',
  'Ah, the Star Charm rests in the stone circle, as it has for three hundred years. The legend says it answers only to togetherness.': '啊，星之护符就安放在石阵里，三百年来一直如此。传说它只回应同心协力的人。',
  'Remarkable. The stones have not sung like that since I was a girl. Take the Star Charm, dears.': '真了不起。自从我还是个小姑娘，石头就没这样唱过。星之护符拿去吧，孩子们。',

  // ---- 终幕
  'Head back to the plaza for the Sky Lantern!': '回广场去放天灯吧！',
  'Look at that — all five Star Charms, home before the first star fell. Friends, you did it!': '看看——五枚星之护符，在第一颗星落下前全回来了。朋友们，你们做到了！',
  'Everyone together now… one, two, three!': '大家一起来……一、二、三！',
  'Same time next year? The stars will be waiting. Thank you for playing, friends!': '明年还是这个时候？星星会等着你们。谢谢你们来玩，朋友们！',
  'What now?': '接下来呢？',
  'Explore the valley together': '一起探索山谷',
  'a night stroll, no rush': '夜里散散步，不赶时间',
  'Play again from the start': '从头再玩一遍',
  'new votes, new winners': '新一轮投票，新的赢家',
  'Back to the lobby': '回到大厅',
  'change outfits, invite friends': '换换装扮，邀请朋友',
  'Free roam': '自由漫游',
  'Free roam! Explore the valley together': '自由漫游！一起探索山谷',
  'the big screen can press L to go back to the lobby': '大屏幕上按 L 就能回到大厅',

  // 称号：给谁都合适（不要有性别指向的词）
  'Starfall Festival Awards': '流星节颁奖',
  'Star of the Festival': '节庆之星',
  'Stardust Collector': '星尘收藏家',
  'Hop Champion': '蹦跳冠军',
  'Hen Whisperer': '母鸡知音',
  'Snowball Sharpshooter': '雪球神射手',
  'Acorn Detective': '橡果侦探',
  'Koi Whisperer': '锦鲤知音',
  'Trailblazer': '开路先锋',
  'Ice Dancer': '冰上舞者',
  'Best Friend': '最佳好友',
  'Heart of the Party': '派对之心',
  '{n} stardust': '{n} 星尘',
  '{n} stardust [one]': '{n} 星尘',   // 英文单复数同形
  '{n} hop': '{n} 次蹦跳',
  '{n} hops': '{n} 次蹦跳',
  '{n} hen': '{n} 只母鸡',
  '{n} hens': '{n} 只母鸡',
  '{n} hit': '{n} 次命中',
  '{n} hits': '{n} 次命中',
  '{n} acorn': '{n} 颗橡果',
  '{n} acorns': '{n} 颗橡果',
  '{n} point': '{n} 分',
  '{n} points': '{n} 分',
  '{n} step': '{n} 步',
  '{n} steps': '{n} 步',
  '{n} s on ice': '{n} 秒冰上时间',

  // 规则卡、倒计时与结算
  'hosted by {who} · {n}s': '主持：{who} · {n} 秒',
  'Press {a} when you’re ready ({n}/{total})': '准备好就按 {a}（{n}/{total}）',
  'GO!': '开始！',
  '{game} — results': '{game} —— 结果',
  '1st': '第 1 名',
  '2nd': '第 2 名',
  '3rd': '第 3 名',
  '{n}th': '第 {n} 名',
  '{n} pt': '{n} 分',
  '{n} pts': '{n} 分',
  'A to continue': '按 A 继续',

  // 冒险期间的大屏幕
  '{n}/{total} here': '已就位 {n}/{total}',
  'waiting for {names}': '等待 {names}',
  'Final: jump together!': '决胜：一起跳！',
  'Round {n}/3': '第 {n}/3 轮',

  // 手机（按钮上的字要短）
  'Ready!': '准备好啦！',
  'Next': '下一位',
  'Wave': '挥手',
  'Get ready…': '准备……',
  'You have ★ {n}': '你有 ★ {n}',
  'Story time — look at the big screen!': '故事时间——看大屏幕！',
  '{goal} — follow the arrow!': '{goal} —— 跟着箭头走！',
  'Free roam! Wander, hop, chat with the villagers': '自由漫游！随便逛、跳一跳、和村民聊聊',

  // ---------------------------------------------------------------- 小游戏
  // 捉鸡大作战
  'Coop {n}/{total}': '鸡舍 {n}/{total}',
  'A golden hen! She’s worth 3!': '一只金母鸡！值 3 分！',
  'Too far!': '太远了！',
  'Grab': '抓住',
  'GRAB!': '抓住！',
  'Carry it to the coop!': '抱回鸡舍！',
  'Catch a hen, bring it to the coop': '抓住母鸡，抱回鸡舍',
  // 雪球大乱斗
  'Throw': '扔',
  'Dodge': '闪避',
  'Brrr! Seeing stars…': '呼——好冷！眼冒金星……',
  'Hit friends & snowmen · jump to dodge': '打中朋友和雪人 · 跳跃闪避',
  // 橡果大搜寻
  'Jump in!': '跳进去！',
  // 钓锦鲤
  'Face the pond!': '面向池塘！',
  'Too soon!': '太早了！',
  'ANCIENT KOI! +5': '远古锦鲤！+5',
  'Golden koi! +3': '金锦鲤！+3',
  'Koi! +1': '锦鲤！+1',
  'It got away…': '它跑掉了……',
  'Reel in': '收线',
  'NOW!!': '就是现在！',
  'Wait for the bite… (your phone buzzes)': '等鱼咬钩……（手机震动）',
  'A BITE! Press A!': '咬钩了！按 A！',
  'Face the pond and cast your line': '面向池塘，抛出鱼线',
  // 星石阵
  'Everyone jump together!': '大家一起跳！',
  'all at the same time…': '要同时哦……',
  'Round {n} complete!': '第 {n} 轮完成！',
  'JUMP!': '跳！',
  'Everyone jump at the same time!': '所有人同时起跳！',
  'Round {n}/3 · everyone on a glowing star!': '第 {n}/3 轮 · 所有人站上发光的星星！',
  '{n}/{total} stars lit': '{n}/{total} 颗星亮起',
  // 房主开始派对；卡住了怎么办
  'Start the party!': '开始派对！',
  'Everyone’s ready — start the party when you like!': '大家都准备好了——你想什么时候开始都行！',
  'Start the party whenever you like (or wait for everyone to be ready)': '随时可以开始派对（也可以等所有人都准备好）',
  '♛ {name} starts the party — walk around!': '♛ {name} 来开始派对——先四处逛逛吧！',
  'Everyone’s ready! ♛ {name} starts the party': '大家都准备好了！♛ {name} 开始派对',
  '♛ {name} starts the party': '♛ {name} 开始派对',
  'Get unstuck': '脱困',
  '{name} got unstuck!': '{name} 脱困了！',
  'Unstuck! ♥': '脱困啦！♥',
  'Get everyone unstuck': '让所有人脱困',
  'anyone stuck in a corner hops to open ground': '卡在角落的人会跳到空地上',
  'World map': '世界地图',
  'Unfolding the map…': '正在展开地图……',
  'World': '世界',
  'Near me': '我附近',
};
