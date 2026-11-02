import unittest
from pathlib import Path

from lupa import LuaRuntime

SCRIPT = (Path(__file__).resolve().parent.parent / 'PBZNoSplineWall/Scripts/main.lua').read_text(encoding='utf-8')
MOCK = r'''
logs={}; print=function(s) logs[#logs+1]=s end
Key={F9=120}; actors={}; channel=2
cap={ IsValid=function() return true end, GetCollisionObjectType=function() return channel end }
player={ CapsuleComponent=cap, IsValid=function() return true end }
require=function(name) assert(name=='UEHelpers'); return { GetPlayer=function() return player end } end
FindAllOf=function(name) assert(name=='BP_SplineWall_C'); return actors end
ExecuteInGameThread=function(fn) fn() end
RegisterKeyBind=function(key,fn) assert(key==Key.F9); toggle=fn end
LoopAsync=function(ms,fn) assert(ms==3000); tick=fn end
function wall(name, initial, persistent)
 local c={valid=true, response={[2]=initial,[3]=2}}
 function c:IsValid() return self.valid end
 function c:GetCollisionResponseToChannel(ch) return self.response[ch] end
 function c:SetCollisionResponseToChannel(ch,v) self.response[ch]=v end
 local a={DynamicMeshComponent=c, valid=true}
 function a:IsValid() return self.valid end
 function a:GetFullName() return (persistent==false and 'Transient:' or 'World:PersistentLevel.')..name end
 return a
end
'''

class RuntimeBehaviour(unittest.TestCase):
    def lua(self):
        lua = LuaRuntime()
        lua.execute(MOCK)
        lua.execute(SCRIPT)
        return lua

    def test_initial_toggle_and_restore_only_original_blockers(self):
        self.lua().execute(r'''
          actors={wall('a',2),wall('b',0),wall('c',1),wall('transient',2,false)}
          tick(); assert(actors[1].DynamicMeshComponent.response[2]==2)
          toggle(); assert(actors[1].DynamicMeshComponent.response[2]==0)
          assert(actors[2].DynamicMeshComponent.response[2]==0 and actors[3].DynamicMeshComponent.response[2]==1)
          assert(actors[4].DynamicMeshComponent.response[2]==2 and actors[1].DynamicMeshComponent.response[3]==2)
          toggle(); assert(actors[1].DynamicMeshComponent.response[2]==2)
          assert(actors[2].DynamicMeshComponent.response[2]==0 and actors[3].DynamicMeshComponent.response[2]==1)
        ''')

    def test_streamed_actor_and_respect_external_change(self):
        self.lua().execute(r'''
          actors={wall('a',2)};toggle();actors[2]=wall('later',2);tick()
          assert(actors[2].DynamicMeshComponent.response[2]==0)
          actors[1].DynamicMeshComponent.response[2]=1
          toggle(); assert(actors[1].DynamicMeshComponent.response[2]==1)
          assert(actors[2].DynamicMeshComponent.response[2]==2)
        ''')

    def test_unexpected_player_channel_does_not_modify(self):
        self.lua().execute(r'''
          actors={wall('a',2)};channel=3;toggle();tick()
          assert(actors[1].DynamicMeshComponent.response[2]==2)
          assert(actors[1].DynamicMeshComponent.response[3]==2)
        ''')

    def test_stale_component_replaced_for_streamed_actor(self):
        self.lua().execute(r'''
          actors={wall('same',2)};toggle();actors[1].DynamicMeshComponent.valid=false
          actors[1]=wall('same',2);tick();assert(actors[1].DynamicMeshComponent.response[2]==0)
          toggle();assert(actors[1].DynamicMeshComponent.response[2]==2)
        ''')

if __name__ == '__main__':
    unittest.main()
