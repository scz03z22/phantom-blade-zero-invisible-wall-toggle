# Nexus Mods description / Nexus Mods 双语项目说明

## Title / 标题

Runtime Invisible Wall Toggle / 实时空气墙开关

## English

Press F9 to temporarily disable a class of invisible barriers in *Phantom Blade Zero*. Press F9 again to restore the responses changed by the mod. Disabled by default at startup; newly loaded matching walls are checked approximately every three seconds.

**Beta:** this only affects `BP_SplineWall_C` dynamic-mesh components and does not remove all invisible barriers or add missing collision to scenery. You may clip into scenery, get stuck, fall out of bounds, or affect progression. Back up saves and return to a safe playable area before restoring the walls.

Requires [game-specific UE4SS](https://github.com/KintaroModding/ue4ss/releases/tag/v3.0.1-1195-g1ceefac8). The prototype was tested with Windows Steam build 26266538; this packaged revision has not yet been independently tested in game. See the repository README and the archive's installation guide for setup and removal.

## 中文

在《影之刃零》中按 F9，临时关闭一类空气墙对玩家的阻挡；再次按 F9 恢复。每次启动默认关闭，启用时约每三秒检查新加载的同类墙体。

**测试版：**本模组只处理 `BP_SplineWall_C` 的动态网格组件，不能移除所有空气墙，也不会为场景补充缺失的碰撞。越界可能导致穿模、卡住、掉出地图或影响任务。建议备份存档，回到正常可玩区域后再恢复空气墙。

需要单独安装[适配游戏的 UE4SS](https://github.com/KintaroModding/ue4ss/releases/tag/v3.0.1-1195-g1ceefac8)。原型在 Windows Steam build 26266538 中测试；本打包版本尚未进行独立实机复测。安装与卸载步骤见仓库 README 和压缩包说明。

## Credits / 说明

UE4SS: UE4SS-RE team and contributors; the game-specific UE4SS package is published by KintaroModding. Neither UE4SS nor game assets are included. Mod code and page text were developed with generative AI under player direction and with gameplay feedback.

UE4SS 由 UE4SS-RE 团队及贡献者开发，游戏适配包由 KintaroModding 发布；本模组不包含 UE4SS 或游戏资源。模组代码与页面文案由生成式 AI 在玩家指导和实机反馈下协助制作。

Nexus submission note: check the current [AI tagging rules](https://help.nexusmods.com/article/28-file-submission-guidelines), including `AI-Generated Content` and `AI Media` where applicable, before publication.
