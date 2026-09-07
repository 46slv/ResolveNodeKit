-- One-shot Fusion-side launcher for the direct Arrange production seam.
--
-- This is not a UI probe.  It loads a disposable .comp, creates a small
-- selected/unselected fixture, and runs the installed Python evidence source
-- through Fusion's own RunScript route.  The result AskUser is intentionally
-- left visible for the external busy/result watcher to observe and close.

local function text(value)
    if value == nil then return "nil" end
    local ok, result = pcall(function() return tostring(value) end)
    if ok then return result end
    return "<unprintable>"
end

local function count_tools(container)
    local count = 0
    for _, _ in pairs(container:GetToolList(false) or {}) do count = count + 1 end
    return count
end

assert(fusion ~= nil, "Fusion endpoint is unavailable")

if arg and arg[1] == "--read-only" then
    local current = fusion:GetCurrentComp()
    assert(current ~= nil, "no current Fusion composition")
    local attrs = current:GetAttrs() or {}
    print("SEAM_READ_ONLY=true NAME=" .. text(attrs.COMPS_Name) ..
        " TOOLS=" .. text(count_tools(current)) ..
        " CURRENT_FRAME=" .. text(current.CurrentFrame))
    return
end

assert(arg and arg[1] and arg[2], "usage: arrange_seam_launcher.lua <fixture.comp> <handler.py> [group]")
local fixture_path = arg[1]
local handler_path = arg[2]
local with_group = arg[3] == "group"

local comp = assert(fusion:LoadComp(fixture_path), "fixture LoadComp failed")
local flow = assert(comp.CurrentFrame and comp.CurrentFrame.FlowView, "fixture FlowView unavailable")

local function add(reg_id, x, y, name)
    local tool = assert(comp:AddTool(reg_id, x, y), "AddTool failed: " .. reg_id)
    assert(tool:SetAttrs({TOOLS_Name = name}) ~= false, "rename failed: " .. name)
    return tool
end

local b1 = add("Background", -4, 0, "RNK_SEAM_B1")
local b2 = add("Background", -4, 2, "RNK_SEAM_B2")
local merge = add("Merge", -2, 1, "RNK_SEAM_M1")
local output = add("MediaOut", 0, 1, "RNK_SEAM_Out")
local u1 = add("Background", 20, 20, "RNK_SEAM_U1")
local u2 = add("Background", 24, 22, "RNK_SEAM_U2")
assert(merge:SetInput("Background", b1.Output) ~= false, "background connection failed")
assert(merge:SetInput("Foreground", b2.Output) ~= false, "foreground connection failed")
assert(output:SetInput("Input", merge.Output) ~= false, "output connection failed")

local group = nil
if with_group then
    group = add("GroupOperator", 8, 1, "RNK_SEAM_Group")
    local child = assert(group:AddTool("Background", 0, 0), "group child AddTool failed")
    assert(child:SetAttrs({TOOLS_Name = "RNK_SEAM_GroupChild"}) ~= false, "group child rename failed")
end

assert(comp:SetActiveTool(nil) ~= false, "selection clear failed")
for _, tool in ipairs({b1, b2, merge, output}) do
    assert(flow:Select(tool, true) ~= false, "selection failed")
end
if with_group then
    assert(flow:Select(group, true) ~= false, "group selection failed")
end

local selected_count = with_group and 5 or 4
print("SEAM_FIXTURE=true TOOLS=" .. text(count_tools(comp)) ..
    " SELECTED=" .. text(selected_count) .. " INCLUDE_UNSELECTED=false UNGROUP=" .. text(with_group))
local ok, result = pcall(function() return fusion:RunScript("Py", handler_path) end)
print("SEAM_HANDLER_RETURN=" .. text(ok) .. " RESULT=" .. text(result))
pcall(function() comp:Close() end)
if not ok then error(result) end
