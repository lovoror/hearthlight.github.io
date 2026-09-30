# Hearthlight — 简体中文（zh）本地化须知

游戏：`Hearthlight`（《炉火之光》）—— 2.5D 像素美术的温馨生活/冒险游戏，单人剧情十章 + 本地派对模式。
目标：把 `src/lang/fr/<name>.js`（法语词典，**键就是英文原文**）逐条翻译成 **简体中文**，写出 `src/lang/zh/<name>.js`。

参考：`tools/i18n/names-zh.json` 是全部短条目（名称、按钮、标签）的中英对照总表，查词先查它；
`node tools/i18n/names.mjs zh` 可重新生成。

## 硬性规则（违反会让 CI 的 i18n 检查失败）

1. **键（`'...'` 左边）绝对不能改、不能增、不能删、顺序保持**。键是英文原文，是程序查找用的 ID。
   键里可能有 `’`、`—`、`♪`、`{p}`、`{q}` 等，必须原样复制。
2. **只翻译值（右边）**。值里若有 `{...}` 形式的东西，必须逐字保留、数量一致：
   - 故事标签：`{p}`（停顿）`{pp}`（长停顿）`{big}` `{shake}` `{gold}` `{/}` 等
   - 变量：`{q}` `{n}` `{item}` `{total}` `{xp}` `{name}` 等
   - 纯格式串（如 `' ({n}/{total})'`、`'+{n} XP'`、`'♪ … ♪'`）几乎不用改，保持即可。
3. **导出名**：`export const CH1_FR = {` → `export const CH1_ZH = {`（其它同理：`MOUNTS_FR`→`MOUNTS_ZH`、`EVENTS_FR`→`EVENTS_ZH`、`CONTROLS_FR`→`CONTROLS_ZH`、`RELEASE9_FR`→`RELEASE9_ZH`、`CLASSES9_FR`→`CLASSES9_ZH`、`MULTI10_FR`→`MULTI10_ZH`、`WORLD13_FR`→`WORLD13_ZH`；没有 `_FR` 后缀的（`UI`、`STORY`、`ITEMS`、`WORLD7`…）保持原样）。
4. **`__group` 块**（如果原文件有）：**键集合必须与法语文件完全一致**，一个都不能少。这是派对模式里对**全队**说的话。
   - 普通条目用单数口吻「你」；`__group` 里的条目用「你们 / 大家」。
   - 如果某句话本来就没有人称区别，`__group` 里可以和普通条目相同。
5. 文件开头 `//` 注释可保留（可译成中文，也可整段保留英文），但**注释里不要出现英文直角撇号 `'`**（翻译脚本会把 `//` 注释里代码后的 `'` 误当成字符串开头）。注释里需要用撇号时用 `’`。
6. 值里**不要用 emoji**，也不要用生僻符号（位图字体只收录了常用汉字与全角标点）。用 **全角中文标点**：`，。！？：；、（）《》「」“”……`，不要用半角 `,` `.` `!` `?`。
7. 数字、`¢`、`XP`、`%`、`HP` 之类保持原样；单位前的**不换行空格** `\u00a0` 若原文有就保留（写成 `\u00a0` 转义）。

## 语气与风格

- 温馨、俏皮、有点童话味；面向全年龄。**单人口吻用「你」，不要用「您」**。
- UI 按钮/标签**要短**：能 2–4 个字最好（中文比法语短，别写长句）。
- 对话保持口语化，不要书面腔，不要逐字硬译。梗和双关尽量换成中文里同样好笑的说法。
- 专有名词务必用下面的**术语表**，跨文件必须一致。

## 术语表（必须遵守）

| English | 中文 |
| --- | --- |
| Hearthlight | 炉火之光 |
| Marigold Cove | 金盏湾 |
| Honeydew Fields | 蜜露田野 |
| Waterfall Lake | 瀑布湖 |
| Driftwood Beach | 浮木滩 |
| Seagull Bluffs | 海鸥崖 |
| Turtle Isle / the Turtle Nest | 龟岛 / 龟巢 |
| Deep Whisperwood | 低语深林 |
| Breezy Hill | 微风丘 |
| Dusty Gulch | 尘沙沟 |
| Croakmire | 蛙鸣沼泽 |
| Frostpeak | 霜峰 |
| Palm Oasis | 棕榈绿洲 |
| Lanternport | 灯笼港 |
| Harvestholm | 丰收堡 |
| Glowtide | 荧光潮 |
| Candlewick | 烛芯镇 |
| Cogsworth | 齿轮镇 |
| Prism Springs | 棱镜泉 |
| Hollowmoor Manor | 幽泽庄园 |
| Saltmirror | 盐镜 |
| Stiltwater | 高脚水乡 |
| Fern Landing | 蕨叶渡 |
| Straits Light | 海峡灯塔 |
| Dawn Monastery | 黎明寺 |
| the Grand Monde | 大千世界 |
| the Murk / murky | 阴霾 |
| the Lamplighters | 点灯人 |
| Party Mode | 派对模式 |
| the Festival Ring | 节庆环 |
| King of the Ring | 圈中王者 |
| the Duchess（Duchess Gloria Gloomsworth） | 阴郁女公爵（格洛丽亚·格鲁姆斯沃斯），简称「女公爵」 |
| Crumble | 碎碎 |
| Minnow | 小鱼 |
| Fidget | 躁躁 |
| Brick | 砖头 |
| Perkins | 珀金斯 |
| Captain Wendeline Gale / Wendy | 温德琳·盖尔船长 / 温迪 |
| Professor Hazel Burrows | 黑兹尔·伯罗斯教授 |
| Old Rowan | 老罗文 |
| Tansy | 坦西 |
| Barley the Miller | 磨坊主巴利 |
| Barkbeard | 树皮胡 |
| Grandmother Tuya | 图雅奶奶 |
| Temur | 铁木尔 |
| Sheriff Dolly | 多莉警长 |
| Old Boom | 老邦 |
| Nugget Nell | 金块奈尔 |
| Foreman Grubb | 格拉布工头 |
| Old Morel | 老羊肚菌 |
| King Croakington | 呱呱王 |
| Sir Newton | 牛顿爵士 |
| Mama Yuki | 雪妈 |
| Tobi | 托比 |
| Sister Nimbus | 尼姆巴斯修女 |
| Auntie Saffron | 藏红花婶婶 |
| Tariq | 塔里克 |
| Elder Shellington | 龟壳长老 |
| Snap | 咔嚓 |
| Zizi | 滋滋 |
| Professor Dotty Ammonite | 多蒂·菊石教授 |
| Old Barnaby | 老巴纳比 |
| Granny Mochi | 麻薯奶奶 |
| Barnacle Bess | 藤壶贝丝 |
| Grandmother Bellows | 风箱奶奶 |
| Old Hoshi | 老星 |
| Abbot Sen | 森方丈 |
| Brother Bao | 包师兄 |
| Blanche the Salt Painter | 盐画师布兰奇 |
| Mei | 梅 |
| Tamsin | 塔姆辛 |
| Mayor Marrow | 马罗市长 |
| Old Mo | 老莫 |
| Warden Ashby | 阿什比守望者 |
| Farmer Hazel | 农夫黑兹尔 |
| Marisol | 玛丽索尔 |
| Wick the Hatter | 帽匠灯芯 |
| Aunt Tallow | 牛脂婶婶 |
| Master Tock | 托克师傅 |
| Ranger Rhoda | 罗达巡林员 |
| Pembroke | 彭布罗克 |
| Mrs Dumpling | 饺子太太 |
| Hob | 霍布 |
| Posy | 波西 |
| Lady Honoria | 霍诺丽亚夫人 |
| Fen / Bo | 芬 / 波 |
| Nana June | 琼奶奶 |
| a Lamplighter | 点灯人 |
| quest / side quest | 任务 / 支线任务 |
| XP / level | 经验值 / 等级 |
| berries / coin | 浆果 / 金币 |
| inventory / shop | 背包 / 商店 |
| host / lobby | 房主 / 大厅 |
| pad（手机手柄） | 手柄 |
| HP / stamina | 生命 / 体力 |

## 文件格式示例（`src/lang/fr/arena.js` → `src/lang/zh/arena.js`）

法语：

```js
// French for the grand Festival Ring (Party v3): King of the Ring, barrels,
// the crowd's treats.
export const ARENA = {
  'King of the Ring': 'Roi du cercle',
  'The golden circle moved!': 'Le cercle doré s’est déplacé !',
  'Barrels! Jump over them with B!': 'Des tonneaux ! Saute par-dessus avec B !',
};
```

中文（注意：注释里用 `’` 而不是 `'`）：

```js
// 节庆环（派对 v3）：圈中王者、木桶、围观群众的点心。
export const ARENA = {
  'King of the Ring': '圈中王者',
  'The golden circle moved!': '金色圆环移动了！',
  'Barrels! Jump over them with B!': '木桶来了！按 B 跳过去！',
};
```

## 交付要求

- 每个文件写完都要能通过 `node --check <文件路径>`（在工作目录 `J:\github\hearthlight.github.io` 下运行）。
- 交付时回报：每个文件的路径、导出名、键的条数（含 `__group` 内的条数）、`node --check` 结果。
