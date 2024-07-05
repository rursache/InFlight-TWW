local InFlight = CreateFrame("Frame", "InFlight")  -- no parent is intentional
local self = InFlight
						 InFlight:SetScript("OnEvent", function(this, event, ...) this[event](this, ...) end)
						 InFlight:RegisterEvent("ADDON_LOADED")

-- LOCAL FUNCTIONS
local function LoadInFlight()
	if not InFlight.ShowOptions then
		LoadAddOn("InFlight")
	end
	return GetAddOnEnableState(UnitName("player"), "InFlight") == 2 and InFlight.ShowOptions and true or nil
end

-----------------------------------------
function InFlight:ADDON_LOADED(addonName)
-----------------------------------------
	if addonName == "InFlight_Load" then
		self:RegisterEvent("TAXIMAP_OPENED")
			if self.SetupInFlight then
				self:SetupInFlight()
			else
				self:UnregisterEvent("ADDON_LOADED")
			end
			elseif addonName == "InFlight" then
				self:UnregisterEvent("ADDON_LOADED")
				self:LoadBulk()
			end
end

-------------------------------------
function InFlight:TAXIMAP_OPENED(...)
-------------------------------------
	if LoadInFlight() then
		local uiMapSystem = ...
		local isTaxiMap = uiMapSystem == Enum.UIMapSystem.Taxi
		self:InitSource(isTaxiMap)
	end
end

-- maybe this stuff gets garbage collected if InFlight isn't loadable
if GetAddOnEnableState(UnitName("player"), "InFlight") == 2 then
	-- GLOBALS -> LOCAL
	local ipairs, strfind = ipairs, strfind
	
	-- LOCALIZATION
	local L = LibStub("AceLocale-3.0"):GetLocale("InFlight", true)
	
	InFlight.L = L

	local t
	do
	t = {
		[L["Amber Ledge"]]								= {{ find = L["AmberLedgeGossip"],				s = "Amber Ledge",								d = "Transitus Shield (Scenic Route)" }},
		[L["Argent Tournament Grounds"]]	= {{ find = L["ArgentTournamentGossip"],	s = "Argent Tournament Grounds",	d = "Return" }},
		[L["Blackwind Landing"]]					= {{ find = L["BlackwindLandingGossip"],	s = "Blackwind Landing",					d = "Skyguard Outpost" }},
		[L["Caverns of Time"]]						= {{ find = L["CavernsOfTimeGossip"],			s = "Caverns of Time",						d = "Nozdormu's Lair" }},
		[L["Expedition Point"]]						= {{ find = L["ExpeditionPointGossip"],		s = "Expedition Point",						d = "Shatter Point" }},
		[L["Hellfire Peninsula"]]					= {{ find = L["HellfirePeninsulaGossip"],	s = "Honor Point",								d = "Shatter Point" }},
		[L["Nighthaven"]]									= {{ find = L["NighthavenGossipA"],				s = "Nighthaven", 								d = "Rut'theran Village" },
											   								{  find = L["NighthavenGossipH"],				s = "Nighthaven", 								d = "Thunder Bluff" }},
		[L["Old Hillsbrad Foothills"]]		= {{ find = L["OldHillsbradGossip"],			s = "Old Hillsbrad Foothills",		d = "Durnholde Keep" }},
    [L["Reaver's Fall"]]		        	= {{ find = L["Reaver'sFallGossip"],			s = "Reaver's Fall",		        	d = "Spinebreaker Post" }},
		[L["Ring of Transference"]]				= {{ find = L["ToBastionGossip1"],				s = "Oribos",											d = "Bastion" },
											   								{  find = L["ToBastionGossip2"],				s = "Oribos",											d = "Bastion" }},
		[L["Shatter Point"]]							= {{ find = L["ShatterPointGossip"],			s = "Shatter Point",							d = "Honor Point" }},
		[L["Skyguard Outpost"]]						= {{ find = L["SkyguardOutpostGossip"],		s = "Skyguard Outpost",						d = "Blackwind Landing" }},
		[L["Stormwind City"]]							= {{ find = L["StormwindCityGossip"],			s = "Stormwind City",							d = "Return" }},
		[L["Sun's Reach Harbor"]]					= {{ find = L["SSSAGossip"],							s = "Shattered Sun Staging Area",	d = "Return" },
											   								{  find = L["SSSAGossip2"],							s = "Shattered Sun Staging Area",	d = "The Sin'loren" }},
		[L["The Sin'loren"]]							= {{ find = L["TheSin'lorenGossip"],			s = "The Sin'loren",							d = "Shattered Sun Staging Area" }},
		[L["Valgarde"]]										= {{ find = L["ValgardeGossip"],					s = "Valgarde",										d = "Explorers' League Outpost" }},
	}
	end


--[[ previus versoning hold ove until release to confirm original code no longer needed
-- support for flightpaths that are started by gossip options
hooksecurefunc("GossipTitleButton_OnClick", function(this, button)
	if this.type ~= "Gossip" then
		return
	end

local subzone = GetMinimapZoneText()

local tsz = t[subzone]
	if not tsz then
		return
	end

local text = this:GetText()
	if not text or text == "" then
		return
	end

local source, destination
	for _, sz in ipairs(tsz) do
		if strfind(text, sz.find, 1, true) then
			source = sz.s
			destination = sz.d
			break
		end
	end

	if source and destination and LoadInFlight() then
		self:StartMiscFlight(source, destination)
		end
	end)
]]--


-- support for flightpaths that are started by gossip options
hooksecurefunc(_G.GossipOptionButtonMixin, "OnClick", function(this, button)
	local elementData = this:GetElementData()
		if elementData.buttonType ~= _G.GOSSIP_BUTTON_TYPE_OPTION then
			return
		end
		
		local subzone = GetMinimapZoneText()
		
		local tsz = t[subzone]
		if not tsz then
			return
		end
		
		local text = this:GetText()
		if not text or text == "" then
			return
		end		               
		
		local source, destination
		for _, sz in ipairs(tsz) do
			if strfind(text, sz.find, 1, true) then
		  	source = sz.s
		  	destination = sz.d
		  	break
			end
		end
		
	if source and destination and LoadInFlight() then
		self:StartMiscFlight(source, destination)
	end
end)                  

	---------------------------------
	function InFlight:SetupInFlight()
	---------------------------------
		SlashCmdList.INFLIGHT = function()
			if LoadInFlight() then
				self:ShowOptions()
			end
		end
		SLASH_INFLIGHT1 = "/inflight"

		local panel = CreateFrame("Frame")
		panel.name = "InFlight"
		panel:SetScript("OnShow", function(this)
			if LoadInFlight() and InFlight.SetLayout then
				InFlight:SetLayout(this)
			end
		end)
		panel:Hide()
		InterfaceOptions_AddCategory(panel)
		InFlight.SetupInFlight = nil
	end
end
