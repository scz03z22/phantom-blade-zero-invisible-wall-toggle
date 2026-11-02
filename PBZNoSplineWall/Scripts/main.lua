-- Disable only the Pawn collision response on loaded BP_SplineWall actors.
-- F9 restores responses changed by this mod; F9 again enables it.
local UEHelpers = require('UEHelpers')
local enabled = false
local changed = {}
local function log(s)
 if not s:match('^ignored ') and not s:match('^restored ') then
  print('[NOSPLINEWALL] '..s..'\n')
 end
end
local function valid(o)
 local ok,v=pcall(function() return o and o:IsValid() end);return ok and v
end
local function status(s) end
local function scan()
 if not enabled then return end
 local p=UEHelpers.GetPlayer();if not valid(p) then return end
 local cap=p.CapsuleComponent;if not valid(cap) then return end
 local channel=cap:GetCollisionObjectType();if channel~=2 then status('unexpected player channel '..tostring(channel));return end
 local actors=FindAllOf('BP_SplineWall_C') or {};local loaded,modified=0,0
 for _,actor in ipairs(actors) do
  local ok,err=pcall(function()
   if not valid(actor) then return end
   local name=actor:GetFullName();if not name:find(':PersistentLevel.',1,true) then return end
   local component=actor.DynamicMeshComponent;if not valid(component) then return end
   loaded=loaded+1
   local current=component:GetCollisionResponseToChannel(channel)
   local record=changed[name]
   if record and not valid(record.component) then changed[name]=nil;record=nil end
   if current==2 then
    if not record then changed[name]={component=component,channel=channel,original=current} end
    component:SetCollisionResponseToChannel(channel,0)
    if component:GetCollisionResponseToChannel(channel)==0 then modified=modified+1;log('ignored '..name) end
   end
  end)
  if not ok then log('scan_actor_error '..tostring(err)) end
 end
 local count=0;for _,record in pairs(changed) do if valid(record.component) then count=count+1 end end
 status('enabled=true\nloaded_spline_walls='..loaded..'\nchanged_live='..count..'\nchanged_this_scan='..modified)
end
local function restore()
 local restored,errors=0,0
 for name,record in pairs(changed) do
  local ok,err=pcall(function()
   if valid(record.component) and record.component:GetCollisionResponseToChannel(record.channel)==0 then
    record.component:SetCollisionResponseToChannel(record.channel,record.original)
    assert(record.component:GetCollisionResponseToChannel(record.channel)==record.original,'readback mismatch')
    restored=restored+1;log('restored '..name)
   end
  end)
  if not ok then errors=errors+1;log('restore_error '..name..' '..tostring(err)) end
 end
 if errors==0 then changed={} end
 status('enabled=false\nrestored='..restored..'\nrestore_errors='..errors)
 log('disabled restored='..restored..' errors='..errors)
end
RegisterKeyBind(Key.F9,function()
 ExecuteInGameThread(function()
  local ok,err=pcall(function()
   enabled=not enabled
   if enabled then log('enabled by F9');scan() else restore() end
  end)
  if not ok then log('toggle_error '..tostring(err)) end
 end)
end)
LoopAsync(3000,function()
 if enabled then ExecuteInGameThread(function() local ok,err=pcall(scan);if not ok then log('scan_error '..tostring(err)) end end) end
 return false
end)
status('enabled=false\nwaiting_for_player=true')
log('loaded; disabled by default; F9 toggles')
