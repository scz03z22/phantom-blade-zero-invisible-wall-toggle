# Phantom Blade Zero — Runtime Invisible Wall Toggle

[中文](#中文) · [English](#english)

## 中文

一个《影之刃零》的 UE4SS Lua 测试模组。游戏中按 **F9**，暂时关闭当前已加载区域中一类空气墙对玩家的阻挡；再次按 F9 恢复。本功能每次启动游戏时默认关闭。

### 工作原理和限制

- 处理 `BP_SplineWall_C` 的 `DynamicMeshComponent`：将其对玩家 Pawn 的碰撞响应设为忽略，不删除墙体，也不改变其他碰撞通道。
- 启用期间约每 **3 秒**检查一次已加载对象，新加载的同类墙可能会有短暂延迟。
- 只处理上述类型和组件，**不能移除所有空气墙**。例如，我们发现一处屋顶的隐藏可行走碰撞不受本模组影响。
- 本模组后续可能会增加对没模型地形的碰撞判定（或者加更贴近的空气墙）来解决穿模跑到地图外的情况，目前codex好像没法很好解决这个问题，有懂的大佬欢迎讨论。
- 没有画面内开关提示；`UE4SS.log` 中可查看带 `[NOSPLINEWALL]` 前缀的加载和切换记录。使用相同按键或修改相同墙体的模组可能冲突。

### 版本和测试情况

当前为 **0.1.0-beta**。原型在 Windows Steam build `26266538` 和适配游戏的 UE4SS `v3.0.1-1195-g1ceefac8` 下测试过：用户确认 F9 可关闭和恢复一处空气墙，并观察到关闭后仍有一些场景模型提供阻挡。本发行包与原型的碰撞逻辑相同，但移除了本机专用日志路径；**发行包尚未完成独立安装后的游戏内复测**。其他游戏版本、商店版本、Linux 和 Steam Deck 尚未验证。

### 安装

1. 关闭游戏，并单独安装[适配《影之刃零》的 UE4SS](https://github.com/KintaroModding/ue4ss/releases/tag/v3.0.1-1195-g1ceefac8)：下载其中的 `phantombladezero_ue4ss` 包，按其说明解压到游戏目录 `platform/steam/`，与较大的 `PBZ.exe` 同目录。**本仓库和模组压缩包不包含 UE4SS。**
2. 下载 [`dist/PBZ_Runtime_Invisible_Wall_Toggle_v0.1.0-beta.zip`](dist/PBZ_Runtime_Invisible_Wall_Toggle_v0.1.0-beta.zip)，把其中的 `PBZNoSplineWall` 文件夹复制到 `platform/steam/ue4ss/Mods/`。最终应有：

   ```text
   PBZ/platform/steam/ue4ss/Mods/PBZNoSplineWall/Scripts/main.lua
   ```

3. 编辑现有的 `platform/steam/ue4ss/Mods/mods.txt`，添加一行 `PBZNoSplineWall : 1`；若已有该条目，只需改为 `1`，不要覆盖其他模组的配置。
4. 启动游戏并读取存档。按 F9 开启；返回安全区域后再次按 F9 恢复。

### 卸载

退出游戏，将 `mods.txt` 中的 `PBZNoSplineWall` 条目删除或设为 `0`，然后仅删除 `Mods/PBZNoSplineWall` 文件夹。不要删除其他模组或 UE4SS。

### 开发与测试

模组源文件在 [`PBZNoSplineWall/Scripts/main.lua`](PBZNoSplineWall/Scripts/main.lua)。`tests/` 中的测试通过模拟 UE4SS 验证默认关闭、开关恢复、加载新墙和碰撞通道保护；它们**不能替代游戏内验证**。在安装了 Python 与 `lupa` 的环境中运行：

```text
python -m unittest discover -s tests -v
```

代码与文档在玩家提出需求、提供实机反馈的过程中由生成式 AI 协助制作；UE4SS 由 UE4SS-RE 团队和贡献者开发。游戏适配的 UE4SS 包由 KintaroModding 发布，本仓库不重新分发这些依赖或游戏资源。代码的再利用权限尚未单独指定。

---

## English

A beta UE4SS Lua mod for *Phantom Blade Zero*. Press **F9** to disable a specific class of invisible wall's collision response to the player; press F9 again to restore the responses changed by the mod. The feature starts disabled on every game launch.

### How it works and limitations

- Targets `DynamicMeshComponent` on `BP_SplineWall_C` actors. It changes the Pawn collision response to Ignore; it does not delete walls or change other collision channels.
- Scans loaded objects approximately every **three seconds** while enabled. Newly streamed walls can take a short time to update.
- It does **not remove all invisible barriers**. For example, a hidden walkable collision surface at a roof was not affected during testing.
- A future version may try to add collision for scenery with missing collision, or move barriers closer to visible surfaces, to reduce clipping and falling outside the map. Codex has not yet been able to solve this reliably; suggestions and discussion are welcome.
- There is no on-screen toggle indicator. Load and toggle messages use the `[NOSPLINEWALL]` prefix in `UE4SS.log`. Mods using F9 or changing the same collisions can conflict.

### Version and testing

This is **0.1.0-beta**. The prototype was tested on Windows, Steam build `26266538`, with the game-specific UE4SS `v3.0.1-1195-g1ceefac8`: the user confirmed that F9 disabled and restored one barrier, and observed that some visible objects still blocked the character while the mod was enabled. This release package retains the prototype's collision logic but removes machine-specific log paths; **the packaged version has not yet been independently reinstalled and tested in game**. Other game versions, storefronts, Linux and Steam Deck are untested.

### Installation

1. Close the game and install the [Phantom Blade Zero-specific UE4SS package](https://github.com/KintaroModding/ue4ss/releases/tag/v3.0.1-1195-g1ceefac8) separately. Choose the `phantombladezero_ue4ss` archive and follow its instructions to extract it into `platform/steam/` beside the large `PBZ.exe`. **UE4SS is not included in this repository or the mod archive.**
2. Download [`dist/PBZ_Runtime_Invisible_Wall_Toggle_v0.1.0-beta.zip`](dist/PBZ_Runtime_Invisible_Wall_Toggle_v0.1.0-beta.zip), then copy its `PBZNoSplineWall` folder into `platform/steam/ue4ss/Mods/`. The result should be:

   ```text
   PBZ/platform/steam/ue4ss/Mods/PBZNoSplineWall/Scripts/main.lua
   ```

3. Add `PBZNoSplineWall : 1` to the existing `platform/steam/ue4ss/Mods/mods.txt`. If an entry already exists, set it to `1`. Do not replace the rest of the file.
4. Start the game and load a save. Press F9 to enable; return to a safe playable area before pressing F9 again to restore collision.

### Uninstall

Exit the game, remove or disable the `PBZNoSplineWall` entry in `mods.txt`, then delete only `Mods/PBZNoSplineWall`. Leave UE4SS and other mods in place.

### Development and tests

The mod source is [`PBZNoSplineWall/Scripts/main.lua`](PBZNoSplineWall/Scripts/main.lua). The `tests/` suite mocks UE4SS to check default-off behavior, restoration, streamed actors and collision-channel safeguards; it **does not replace in-game testing**. With Python and `lupa` installed:

```text
python -m unittest discover -s tests -v
```

Code and documentation were developed with generative AI under player direction and with gameplay feedback. UE4SS is made by the UE4SS-RE team and contributors; the separate game-specific package is published by KintaroModding. This repository does not redistribute those dependencies or game assets. Reuse permissions for this mod's code have not yet been specified separately.
