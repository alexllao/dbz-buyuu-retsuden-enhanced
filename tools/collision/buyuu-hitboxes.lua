-- Buyuu Retsuden (Japan): native collision rectangles, read-only Gens-rr viewer.
-- No ROM/RAM writes, input changes, guessed sprite bounds or balance edits.
-- API: https://github.com/TASEmulators/gens-rerecording/blob/master/Gens-rr/Output/LuaSamples/gens-lua.html
-- Native proof: pose table 0x19E6CE; loader 0x11C1E..0x11C9A;
-- world box clamp 0x12434..0x1246C; renderer Y+32 at 0x8972..0x89C8.

local OPTIONS = {
    -- 1 aligns most observed sprite uploads; 0 shows immediate RAM.
    -- This is a display aid, not a universal promise about visible VRAM poses.
    FRAME_DELAY = 1,
    push = true,
    hurt = true,
    hit = true,
    guard = true,
    labels = true,
    legend = true,
    actor_info = true
}

local PLAYERS = {
    {base = 0xFFE75E, name = "P1"},
    {base = 0xFFE886, name = "P2"}
}

local STYLES = {
    push  = {fill = 0xFFFF0020, line = 0xFFFF00FF},
    hurt  = {fill = 0x00FF0020, line = 0x00FF00FF},
    hit   = {fill = 0xFF303038, line = 0xFF3030FF},
    guard = {fill = 0x4080FF20, line = 0x4080FFFF}
}

local SLOT_KIND = {"push", "push", "hurt", "hurt", "hit", "hit", "guard", "guard"}
local actors = {}
local history = {}
local last_counter = nil
local FRAME_DELAY = math.max(0, math.floor(tonumber(OPTIONS.FRAME_DELAY) or 1))

local function rb(address)
    return memory.readbyte(address)
end

local function rw(address)
    return memory.readword(address)
end

local function s8(value)
    if value >= 128 then return value - 256 end
    return value
end

local function s16(value)
    value = value % 65536
    if value >= 32768 then return value - 65536 end
    return value
end

local function native_world_edge(world, cached_offset)
    -- The game adds the signed cached byte to a word, then clamps negatives.
    return math.max(0, s16(world + cached_offset))
end

local function read_actor(player)
    local base = player.base
    local world_x, world_y = rw(base + 0x0A), rw(base + 0x10)
    local cam_x, cam_y = s16(rw(base + 0x16)), s16(rw(base + 0x18))
    -- BTST.B #7, actor+$1E: this is the HIGH byte of the word at +$1E.
    local attack_active = rb(base + 0x1E) >= 128
    local actor = {
        name = player.name,
        id = rb(base + 0x58),
        pose = rb(base + 0x04), -- Logical pose in THIS sampled actor, not VRAM.
        action = rb(base + 0x5B),
        hp = rw(base + 0x24),
        attack_active = attack_active,
        boxes = {}
    }
    for slot = 0, 7 do
        local offset = base + 0x5C + slot * 4
        local kind = SLOT_KIND[slot + 1]
        -- The native loader's disabled sentinel is the FIRST byte, 0x80.
        -- Do not flip again: facing and +$0E/+$14 are already in this cache.
        if rb(offset) ~= 0x80 and (kind ~= "hit" or attack_active) then
            local x1 = native_world_edge(world_x, s8(rb(offset))) - cam_x
            local y1 = native_world_edge(world_y, s8(rb(offset + 1))) - cam_y + 32
            local x2 = native_world_edge(world_x, s8(rb(offset + 2))) - cam_x
            local y2 = native_world_edge(world_y, s8(rb(offset + 3))) - cam_y + 32
            actor.boxes[#actor.boxes + 1] = {
                kind = kind, slot = slot,
                x1 = math.min(x1, x2), y1 = math.min(y1, y2),
                x2 = math.max(x1, x2), y2 = math.max(y1, y2)
            }
        end
    end
    return actor
end

local function capture()
    local captured = {}
    for _, player in ipairs(PLAYERS) do
        captured[#captured + 1] = read_actor(player)
    end
    local counter = rw(0xFFE6A8)
    local reset = false
    if actors[1] and actors[2] then
        reset = actors[1].id ~= captured[1].id or actors[2].id ~= captured[2].id
        -- Avoid reusing old-match boxes after a KO/restart or state rewind.
        if (actors[1].hp == 0 and captured[1].hp > 0)
            or (actors[2].hp == 0 and captured[2].hp > 0) then
            reset = true
        end
    end
    if last_counter and counter < last_counter and last_counter - counter < 32768 then
        reset = true -- A rewind/reset, excluding the ordinary 16-bit wrap.
    end
    if reset then history = {} end
    actors = captured
    history[#history + 1] = captured
    while #history > math.max(3, FRAME_DELAY + 1) do
        table.remove(history, 1)
    end
    last_counter = counter
end

local function draw()
    local shown = actors
    local warmup = FRAME_DELAY > 0 and #history <= FRAME_DELAY
    if not warmup then shown = history[#history - FRAME_DELAY] or actors end
    for index, actor in ipairs(shown) do
        if actor.id <= 10 then
            for _, box in ipairs(actor.boxes) do
                if OPTIONS[box.kind] then
                    local style = STYLES[box.kind]
                    gui.box(box.x1, box.y1, box.x2, box.y2, style.fill, style.line)
                    if OPTIONS.labels then
                        gui.text(box.x1, box.y1 - 7,
                            actor.name .. " " .. box.kind .. box.slot, style.line, 0x000000C0)
                    end
                end
            end
            if OPTIONS.actor_info then
                gui.text(index == 1 and 2 or 166, 35,
                    string.format("%s boxpose:%02X act:%02X hit:%s", actor.name,
                        actor.pose, actor.action, actor.attack_active and "ON" or "off"),
                    0xFFFFFFFF, 0x000000C0)
            end
        end
    end
    if OPTIONS.legend then
        gui.text(2, 207, "PUSH", STYLES.push.line, 0x000000C0)
        gui.text(45, 207, "HURT", STYLES.hurt.line, 0x000000C0)
        gui.text(88, 207, "HIT active", STYLES.hit.line, 0x000000C0)
        gui.text(170, 207, "GUARD", STYLES.guard.line, 0x000000C0)
        gui.text(2, 215, "RAM display delay" .. FRAME_DELAY .. (warmup and " warmup" or ""),
            0xFFFFFFFF, 0x000000C0)
    end
end

-- Read after emulation and draw only in the GUI callback, without a competing
-- frameadvance loop. This uses native 320x224 screen coordinates, not 2x PNGs.
capture()
gens.registerafter(capture)
gui.register(draw)
print("Buyuu native boxes: read-only. RAM display delay" .. FRAME_DELAY .. ". Red = sampled active attack only.")
