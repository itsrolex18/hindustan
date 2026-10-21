import os, json, requests, secrets
from datetime import datetime, date, timedelta
from flask import Flask, render_template_string, request, session, redirect, jsonify, make_response
from functools import wraps

SECRET_KEY      = "Hindustan_Osint_Key"
ADMIN_USERNAME  = "Rolexbhaiya"
ADMIN_PASSWORD  = "Hindustan*vX3z"
SECRET_AUTH_KEY = "Hindustan@T9#q"
DB_FILE         = "database.json"
TELEGRAM_LINK   = "https://t.me/Hindustanhack"
BANNER_IMAGE    = "https://i.ibb.co/fV1pw1Lz/IMG-20260505-105056-474.png"

BRAND_ICONS = {
    'fa-instagram','fa-square-instagram','fa-instagram-square','fa-whatsapp','fa-square-whatsapp','fa-whatsapp-square',
    'fa-facebook','fa-facebook-f','fa-square-facebook','fa-facebook-square','fa-messenger','fa-twitter','fa-square-twitter',
    'fa-twitter-square','fa-x-twitter','fa-square-x-twitter','fa-telegram','fa-square-telegram','fa-snapchat',
    'fa-square-snapchat','fa-snapchat-ghost','fa-snapchat-square','fa-github','fa-square-github','fa-github-alt',
    'fa-youtube','fa-square-youtube','fa-tiktok','fa-square-tiktok','fa-linkedin','fa-linkedin-in','fa-square-linkedin',
    'fa-reddit','fa-reddit-alien','fa-square-reddit','fa-discord','fa-square-discord','fa-pinterest','fa-pinterest-p',
    'fa-square-pinterest','fa-tumblr','fa-square-tumblr','fa-twitch','fa-square-twitch','fa-weixin','fa-weibo','fa-qq',
    'fa-line','fa-skype','fa-square-skype','fa-vk','fa-square-vk','fa-mastodon','fa-square-mastodon','fa-bluesky',
    'fa-square-bluesky','fa-threads','fa-square-threads','fa-android','fa-apple','fa-windows','fa-linux','fa-ubuntu',
    'fa-chrome','fa-firefox','fa-firefox-browser','fa-edge','fa-safari','fa-opera','fa-brave','fa-python','fa-js',
    'fa-square-js','fa-node-js','fa-node','fa-react','fa-vuejs','fa-angular','fa-docker','fa-aws','fa-google',
    'fa-google-pay','fa-microsoft','fa-php','fa-java','fa-rust','fa-golang','fa-swift','fa-r-project','fa-npm','fa-yarn',
    'fa-git-alt','fa-gitlab','fa-bitbucket','fa-centos','fa-fedora','fa-redhat','fa-debian','fa-suse','fa-bitcoin','fa-btc',
    'fa-ethereum','fa-eth','fa-monero','fa-cc-visa','fa-cc-mastercard','fa-cc-paypal','fa-cc-amex','fa-cc-stripe',
    'fa-cc-apple-pay','fa-cc-amazon-pay','fa-cc-discover','fa-cc-diners-club','fa-cc-jcb','fa-paypal','fa-stripe','fa-stripe-s',
    'fa-amazon','fa-amazon-pay','fa-ebay','fa-alipay','fa-apple-pay','fa-google-wallet','fa-steam','fa-steam-symbol',
    'fa-playstation','fa-xbox','fa-nintendo-switch','fa-medium','fa-medium-m','fa-dev','fa-hacker-news','fa-product-hunt',
    'fa-codepen','fa-stack-overflow','fa-stack-exchange','fa-digg','fa-delicious','fa-slack','fa-slack-hash','fa-figma',
    'fa-sketch','fa-dribbble','fa-behance','fa-behance-square','fa-flickr','fa-vimeo','fa-vimeo-v','fa-soundcloud',
    'fa-spotify','fa-apple-music','fa-itch-io','fa-etsy','fa-shopify','fa-squarespace','fa-wix','fa-wordpress',
    'fa-wordpress-simple','fa-patreon','fa-buymeacoffee','fa-kickstarter','fa-google-play','fa-app-store','fa-app-store-ios',
    'fa-waze','fa-uber','fa-airbnb','fa-yelp','fa-tripadvisor','fa-foursquare','fa-d-and-d','fa-d-and-d-beyond','fa-dungeon',
    'fa-dragon','fa-dice-d20','fa-orcid','fa-researchgate',
}
def fa_prefix(icon):
    if not icon: return 'fas'
    return 'fab' if icon in BRAND_ICONS else 'fas'

ICON_ALIASES = {
    'fa-radar': 'fa-satellite-dish','fa-binoculars': 'fa-magnifying-glass','fa-telescope': 'fa-magnifying-glass-chart',
    'fa-signal-messenger': 'fa-comment-dots','fa-viber': 'fa-phone','fa-kik': 'fa-comment','fa-user-circle': 'fa-circle-user',
    'fa-money-bill-1': 'fa-money-bill','fa-phone-square': 'fa-square-phone','fa-tachometer-alt': 'fa-gauge-high',
    'fa-map-marker-alt': 'fa-location-dot','fa-check-circle': 'fa-circle-check','fa-times-circle': 'fa-circle-xmark',
    'fa-info-circle': 'fa-circle-info','fa-question-circle': 'fa-circle-question','fa-exclamation-circle': 'fa-circle-exclamation',
    'fa-exclamation-triangle': 'fa-triangle-exclamation','fa-arrow-circle-right': 'fa-circle-arrow-right',
    'fa-arrow-circle-left': 'fa-circle-arrow-left','fa-arrow-circle-up': 'fa-circle-arrow-up','fa-arrow-circle-down': 'fa-circle-arrow-down',
    'fa-edit': 'fa-pen-to-square','fa-trash-alt': 'fa-trash-can','fa-save': 'fa-floppy-disk','fa-home': 'fa-house',
    'fa-mobile-alt': 'fa-mobile-screen','fa-search': 'fa-magnifying-glass','fa-sync': 'fa-arrows-rotate',
    'fa-sync-alt': 'fa-arrows-rotate','fa-redo': 'fa-arrow-rotate-right','fa-undo': 'fa-arrow-rotate-left',
    'fa-cog': 'fa-gear','fa-cogs': 'fa-gears','fa-dashboard': 'fa-gauge-high','fa-sign-out-alt': 'fa-right-from-bracket',
    'fa-sign-in-alt': 'fa-right-to-bracket','fa-globe-asia': 'fa-earth-asia','fa-globe-americas': 'fa-earth-americas',
    'fa-globe-europe': 'fa-earth-europe','fa-globe-africa': 'fa-earth-africa','fa-arrow-left-arrow-right': 'fa-right-left',
    'fa-chart-bar': 'fa-chart-simple','fa-smile': 'fa-face-smile','fa-frown': 'fa-face-frown','fa-meh': 'fa-face-meh',
    'fa-tools': 'fa-screwdriver-wrench',
}
def normalize_icon(icon):
    if not icon: return 'fa-plug'
    icon = str(icon).strip()
    for p in ('fas ','fab ','far ','fal ','fat ','fad '):
        if icon.startswith(p): icon = icon[len(p):]
    if not icon.startswith('fa-'): icon = 'fa-' + icon
    return ICON_ALIASES.get(icon, icon)

# ONLY OSINT & LEAK FEATURES (Removed Call Tracer, RC, Vehicle, DL, etc.)
STANDARD_APIS = {
    'number':{'param':'num','name':'Mobile Lookup'},'number_adv':{'param':'num','name':'Adv Number Info'},
    'number_info':{'param':'num','name':'Basic Num Info'},'number_full':{'param':'num','name':'Number Full Details'},
    'number_alt':{'param':'num','name':'Alternate Number'},'num_operator':{'param':'num','name':'Operator Lookup'},
    'truecaller':{'param':'num','name':'Truecaller Pro'},'truecaller_adv':{'param':'num','name':'Truecaller Advanced'},
    'num_loc':{'param':'num','name':'Number Location'},
    'aadhar':{'param':'num','name':'Aadhar Info'},'aadhar_adv':{'param':'num','name':'Aadhar Advanced'},
    'adharfamily':{'param':'num','name':'Aadhar Family'},'adharfamily_adv':{'param':'num','name':'Family Advanced'},
    'adharration':{'param':'num','name':'Aadhar Ration'},'adharration_adv':{'param':'num','name':'Ration Advanced'},
    'aadhar_dob':{'param':'num','name':'Aadhar DOB'},'aadhar_addr':{'param':'num','name':'Aadhar Address'},
    'voter':{'param':'num','name':'Voter ID Info'},'voter_adv':{'param':'num','name':'Voter Advanced'},
    'pan':{'param':'pan','name':'PAN Verification'},'pan_adv':{'param':'pan','name':'PAN Advanced'},
    'pan_full':{'param':'pan','name':'PAN Full Details'},'pan_dob':{'param':'pan','name':'PAN DOB Lookup'},
    'gst':{'param':'gst','name':'GST Details'},'gst_adv':{'param':'gst','name':'GST Advanced'},
    'gst_full':{'param':'gst','name':'GST Full Details'},'gst_verify':{'param':'gst','name':'GST Verify'},
    'upi':{'param':'upi','name':'UPI Details'},'upi_adv':{'param':'upi','name':'UPI Advanced'},
    'upi_full':{'param':'upi','name':'UPI Full Info'},'upi_bank':{'param':'upi','name':'UPI Bank Info'},
    'ifsc':{'param':'ifsc','name':'Bank IFSC Info'},'ifsc_adv':{'param':'ifsc','name':'IFSC Advanced'},
    'ifsc_branch':{'param':'ifsc','name':'IFSC Branch'},'ifsc_micr':{'param':'ifsc','name':'IFSC MICR'},
    'email':{'param':'mail','name':'Email OSINT'},'email-lookup':{'param':'mail','name':'Email Lookup'},
    'email_adv':{'param':'mail','name':'Email Advanced'},'email_breach':{'param':'mail','name':'Email Breach'},
    'email_gravatar':{'param':'mail','name':'Gravatar Lookup'},
    'insta':{'param':'username','name':'Insta Info'},'insta_adv':{'param':'username','name':'Insta Advanced'},
    'insta_full':{'param':'username','name':'Insta Full'},'insta_email':{'param':'username','name':'Insta to Email'},
    'git':{'param':'username','name':'GitHub Info'},'git_adv':{'param':'username','name':'GitHub Advanced'},
    'git_repo':{'param':'username','name':'GitHub Repos'},'tg':{'param':'info','name':'Telegram Info'},
    'tg_adv':{'param':'info','name':'Telegram Advanced'},'tg_info':{'param':'info','name':'Telegram Details'},
    'snap':{'param':'username','name':'Snapchat Info'},'snap_adv':{'param':'username','name':'Snapchat Advanced'},
    'tw':{'param':'username','name':'Twitter / X Info'},'tw_adv':{'param':'username','name':'Twitter Advanced'},
    'fb':{'param':'username','name':'Facebook Info'},'fb_adv':{'param':'username','name':'Facebook Advanced'},
    'li':{'param':'username','name':'LinkedIn Info'},'li_adv':{'param':'username','name':'LinkedIn Advanced'},
    'yt':{'param':'username','name':'YouTube Info'},
    'ff':{'param':'uid','name':'Free Fire Profile'},'ff_adv':{'param':'uid','name':'FF Advanced'},
    'ff_full':{'param':'uid','name':'FF Full Details'},'bgmi':{'param':'uid','name':'BGMI Profile'},
    'bgmi_adv':{'param':'uid','name':'BGMI Advanced'},'bgmi_full':{'param':'uid','name':'BGMI Full'},
    'ip':{'param':'ip','name':'IP Lookup'},'ip_adv':{'param':'ip','name':'IP Advanced'},
    'ip_geo':{'param':'ip','name':'IP Geolocation'},'whois':{'param':'domain','name':'WHOIS Lookup'},
    'pincode':{'param':'pin','name':'Pincode Info'},'pincode_adv':{'param':'pin','name':'Pincode Advanced'},
    'imei':{'param':'imei','name':'IMEI Tracker'},'imei_adv':{'param':'imei','name':'IMEI Advanced'},
    'imei_full':{'param':'imei','name':'IMEI Full'},
    'crypto':{'param':'addr','name':'Crypto Wallet'},'crypto_adv':{'param':'addr','name':'Crypto Advanced'},
    'leak':{'param':'query','name':'Leak Lookup'},'leak_adv':{'param':'query','name':'Leak Advanced'},
    'username':{'param':'query','name':'Username Search'},'username_adv':{'param':'query','name':'Username Advanced'}
}

FA_DEFAULTS = {
    'number':'fa-phone','number_adv':'fa-phone-volume','number_info':'fa-circle-info','number_full':'fa-address-card',
    'number_alt':'fa-phone-flip','num_operator':'fa-tower-broadcast','truecaller':'fa-circle-check','truecaller_adv':'fa-address-book',
    'num_loc':'fa-location-crosshairs','aadhar':'fa-id-card','aadhar_adv':'fa-id-card-clip','adharfamily':'fa-users',
    'adharfamily_adv':'fa-people-group','adharration':'fa-wheat-awn','adharration_adv':'fa-bowl-food',
    'aadhar_dob':'fa-calendar-days','aadhar_addr':'fa-house-user','voter':'fa-id-badge','voter_adv':'fa-file-shield',
    'pan':'fa-credit-card','pan_adv':'fa-id-card','pan_full':'fa-address-card','pan_dob':'fa-calendar',
    'gst':'fa-building','gst_adv':'fa-building-columns','gst_full':'fa-file-invoice','gst_verify':'fa-circle-check',
    'upi':'fa-money-bill-wave','upi_adv':'fa-indian-rupee-sign','upi_full':'fa-wallet','upi_bank':'fa-building-columns',
    'ifsc':'fa-building-columns','ifsc_adv':'fa-money-check','ifsc_branch':'fa-location-dot','ifsc_micr':'fa-barcode',
    'email':'fa-envelope','email-lookup':'fa-envelope-open','email_adv':'fa-envelope-circle-check','email_breach':'fa-shield-halved',
    'email_gravatar':'fa-circle-user','insta':'fa-instagram','insta_adv':'fa-instagram','insta_full':'fa-instagram',
    'insta_email':'fa-envelope','git':'fa-github','git_adv':'fa-github','git_repo':'fa-code-branch','tg':'fa-telegram',
    'tg_adv':'fa-telegram','tg_info':'fa-circle-info','snap':'fa-snapchat','snap_adv':'fa-snapchat','tw':'fa-x-twitter',
    'tw_adv':'fa-x-twitter','fb':'fa-facebook','fb_adv':'fa-facebook','li':'fa-linkedin','li_adv':'fa-linkedin','yt':'fa-youtube',
    'ff':'fa-fire','ff_adv':'fa-fire-flame-curved','ff_full':'fa-fire','bgmi':'fa-gamepad','bgmi_adv':'fa-gamepad',
    'bgmi_full':'fa-gamepad','ip':'fa-globe','ip_adv':'fa-network-wired','ip_geo':'fa-location-dot','whois':'fa-circle-info',
    'pincode':'fa-location-dot','pincode_adv':'fa-map-location-dot','imei':'fa-magnifying-glass','imei_adv':'fa-mobile-screen',
    'imei_full':'fa-mobile','crypto':'fa-bitcoin','crypto_adv':'fa-ethereum','leak':'fa-database','leak_adv':'fa-server',
    'username':'fa-at','username_adv':'fa-user-secret'
}

AUTO_ICON_MAP = {
    'instagram':'fa-instagram','insta':'fa-instagram','ig':'fa-instagram','whatsapp':'fa-whatsapp','wa':'fa-whatsapp',
    'facebook':'fa-facebook','fb':'fa-facebook','twitter':'fa-twitter','x':'fa-x-twitter','telegram':'fa-telegram',
    'tg':'fa-telegram','snapchat':'fa-snapchat','snap':'fa-snapchat','github':'fa-github','git':'fa-github','youtube':'fa-youtube',
    'yt':'fa-youtube','tiktok':'fa-tiktok','linkedin':'fa-linkedin','reddit':'fa-reddit','discord':'fa-discord',
    'pinterest':'fa-pinterest','twitch':'fa-twitch','wechat':'fa-weixin','weixin':'fa-weixin','skype':'fa-skype','vk':'fa-vk',
    'mastodon':'fa-mastodon','bluesky':'fa-bluesky','threads':'fa-threads','phone':'fa-phone','mobile':'fa-mobile-screen',
    'number':'fa-phone','call':'fa-phone','sim':'fa-sim-card','imei':'fa-magnifying-glass','aadhar':'fa-id-card',
    'aadhaar':'fa-id-card','adhar':'fa-id-card','voter':'fa-id-badge','pan':'fa-credit-card','passport':'fa-passport',
    'dl':'fa-id-card','license':'fa-id-card','licence':'fa-id-card','family':'fa-users','ration':'fa-wheat-awn',
    'truecaller':'fa-circle-check','true':'fa-circle-check','vehicle':'fa-car','car':'fa-car','rc':'fa-file-lines',
    'challan':'fa-receipt','fastag':'fa-bolt','fast':'fa-bolt','truck':'fa-truck','bike':'fa-motorcycle',
    'motorcycle':'fa-motorcycle','num2veh':'fa-right-left','apex':'fa-mobile-screen','driving':'fa-id-card',
    'upi':'fa-money-bill-wave','bank':'fa-building-columns','ifsc':'fa-building-columns','gst':'fa-building',
    'card':'fa-credit-card','wallet':'fa-wallet','paytm':'fa-wallet','phonepe':'fa-wallet','gpay':'fa-wallet',
    'crypto':'fa-bitcoin','bitcoin':'fa-bitcoin','eth':'fa-ethereum','ethereum':'fa-ethereum','ip':'fa-globe',
    'dns':'fa-server','whois':'fa-circle-info','port':'fa-network-wired','wifi':'fa-wifi','mac':'fa-microchip',
    'email':'fa-envelope','mail':'fa-envelope','gmail':'fa-envelope','pincode':'fa-location-dot','pin':'fa-location-dot',
    'address':'fa-location-dot','map':'fa-map-location-dot','location':'fa-location-dot','gps':'fa-location-dot','geo':'fa-globe',
    'freefire':'fa-fire','ff':'fa-fire','bgmi':'fa-gamepad','pubg':'fa-gamepad','cod':'fa-gamepad','valorant':'fa-gamepad',
    'roblox':'fa-gamepad','leak':'fa-database','breach':'fa-database','osint':'fa-magnifying-glass','search':'fa-magnifying-glass',
    'lookup':'fa-magnifying-glass','track':'fa-satellite-dish','tracker':'fa-satellite-dish','spy':'fa-user-secret',
    'hack':'fa-skull-crossbones','dark':'fa-skull-crossbones','news':'fa-newspaper','shop':'fa-store','store':'fa-store',
    'music':'fa-music','video':'fa-video','camera':'fa-camera','photo':'fa-camera','image':'fa-image','file':'fa-file-lines',
    'pdf':'fa-file-pdf','doc':'fa-file-lines','folder':'fa-folder','cloud':'fa-cloud','weather':'fa-cloud-sun',
    'flight':'fa-plane','train':'fa-train','bus':'fa-bus','hotel':'fa-hotel','food':'fa-utensils','health':'fa-heart-pulse',
    'medical':'fa-stethoscope','doctor':'fa-user-doctor','hospital':'fa-hospital','police':'fa-shield-halved',
    'govt':'fa-landmark','court':'fa-gavel','user':'fa-user','name':'fa-user-tie','username':'fa-at','exif':'fa-image',
    'domain':'fa-globe','host':'fa-server',
}
def auto_icon_for(name):
    if not name: return None
    n = str(name).lower().replace('-', '').replace('_', '').replace(' ', '')
    for kw, icon in AUTO_ICON_MAP.items():
        if n == kw: return icon
    for kw in sorted(AUTO_ICON_MAP.keys(), key=len, reverse=True):
        if kw in n: return AUTO_ICON_MAP[kw]
    return None

ICON_CHOICES = [
    "fa-id-card","fa-id-card-clip","fa-id-badge","fa-address-card","fa-address-book",
    "fa-user","fa-user-tie","fa-user-secret","fa-user-shield","fa-user-lock","fa-user-gear",
    "fa-user-pen","fa-user-xmark","fa-user-check","fa-user-clock","fa-user-group","fa-user-plus",
    "fa-user-minus","fa-user-slash","fa-user-tag","fa-user-ninja","fa-user-astronaut",
    "fa-user-graduate","fa-user-nurse","fa-user-doctor","fa-users","fa-people-group",
    "fa-people-arrows","fa-people-roof","fa-fingerprint","fa-passport","fa-circle-user",
    "fa-phone","fa-phone-volume","fa-phone-flip","fa-phone-slash","fa-phone-office","fa-tty",
    "fa-mobile-screen","fa-mobile","fa-mobile-button","fa-mobile-screen-button","fa-sim-card",
    "fa-location-crosshairs","fa-location-dot","fa-location-arrow","fa-map","fa-map-pin",
    "fa-map-location-dot","fa-compass","fa-route","fa-satellite-dish","fa-satellite",
    "fa-tower-broadcast","fa-tower-cell","fa-signal","fa-wifi","fa-wifi-slash","fa-ethernet",
    "fa-router","fa-network-wired","fa-server","fa-globe","fa-earth-africa","fa-earth-americas",
    "fa-earth-asia","fa-earth-europe","fa-earth-oceania",
    "fa-hard-drive","fa-sd-card","fa-usb","fa-memory","fa-microchip","fa-laptop","fa-desktop",
    "fa-computer","fa-display","fa-keyboard","fa-mouse","fa-print","fa-fax","fa-headset",
    "fa-headphones","fa-microphone","fa-speaker","fa-webcam",
    "fa-car","fa-car-side","fa-car-rear","fa-car-battery","fa-truck","fa-truck-fast",
    "fa-truck-pickup","fa-tractor","fa-motorcycle","fa-bicycle","fa-gas-pump","fa-charging-station",
    "fa-bolt","fa-traffic-light","fa-plane","fa-plane-departure","fa-plane-arrival","fa-rocket",
    "fa-helicopter","fa-jet-fighter","fa-ship","fa-anchor","fa-train","fa-train-subway",
    "fa-subway","fa-bus","fa-van-shuttle","fa-taxi",
    "fa-credit-card","fa-money-bill","fa-money-bill-wave","fa-money-bill-transfer",
    "fa-money-bill-trend-up","fa-money-check","fa-money-check-dollar","fa-coins","fa-sack-dollar",
    "fa-vault","fa-piggy-bank","fa-hand-holding-dollar","fa-receipt","fa-wallet",
    "fa-building-columns","fa-building","fa-city","fa-warehouse","fa-industry","fa-landmark",
    "fa-landmark-dome","fa-landmark-flag","fa-house","fa-house-chimney","fa-house-user",
    "fa-hotel","fa-store","fa-shop","fa-hospital","fa-school",
    "fa-indian-rupee-sign","fa-dollar-sign","fa-euro-sign","fa-sterling-sign","fa-yen-sign",
    "fa-won-sign","fa-tenge-sign","fa-bitcoin-sign","fa-percent","fa-hashtag",
    "fa-barcode","fa-qrcode",
    "fa-camera","fa-video","fa-image","fa-photo-film","fa-film","fa-clapperboard",
    "fa-comment","fa-comments","fa-comment-dots","fa-comment-slash","fa-message","fa-messages",
    "fa-comment-medical","fa-envelope","fa-envelope-open","fa-envelope-circle-check",
    "fa-envelopes-bulk","fa-at","fa-inbox","fa-paperclip","fa-paper-plane","fa-mail-forward",
    "fa-mail-reply","fa-ghost","fa-robot","fa-alien","fa-mask","fa-hat-wizard",
    "fa-wand-magic-sparkles","fa-broom",
    "fa-flag","fa-flag-checkered","fa-shield","fa-shield-halved","fa-shield-heart",
    "fa-lock","fa-lock-open","fa-unlock","fa-key",
    "fa-database","fa-clipboard","fa-clipboard-list","fa-clipboard-check","fa-skull",
    "fa-skull-crossbones","fa-bone","fa-eyes","fa-eye","fa-eye-slash",
    "fa-stethoscope","fa-heart","fa-heart-pulse","fa-pills","fa-syringe","fa-tablets",
    "fa-capsules","fa-vial","fa-vials","fa-bacteria","fa-virus","fa-virus-covid",
    "fa-hand-holding-medical",
    "fa-gavel","fa-scale-balanced","fa-star","fa-star-half","fa-star-of-life","fa-crown",
    "fa-gem","fa-ring","fa-trophy","fa-medal","fa-award","fa-certificate",
    "fa-gamepad","fa-fire","fa-fire-flame-curved","fa-dice","fa-dice-d20","fa-dice-d6",
    "fa-chess","fa-chess-knight","fa-chess-queen","fa-chess-king","fa-chess-rook",
    "fa-puzzle-piece","fa-steam","fa-playstation","fa-xbox","fa-dragon",
    "fa-code","fa-code-branch","fa-code-commit","fa-code-merge","fa-code-pull-request",
    "fa-terminal","fa-bug","fa-bug-slash","fa-spider",
    "fa-download","fa-upload","fa-share","fa-share-nodes","fa-link","fa-link-slash","fa-unlink",
    "fa-bell","fa-bell-slash","fa-clock","fa-clock-rotate-left","fa-stopwatch","fa-hourglass",
    "fa-hourglass-half","fa-arrows-rotate","fa-rotate","fa-refresh","fa-power-off","fa-toggle-on",
    "fa-toggle-off","fa-arrow-up","fa-arrow-down","fa-arrow-left","fa-arrow-right",
    "fa-arrow-up-right-from-square","fa-arrow-right-from-bracket","fa-arrow-right-to-bracket",
    "fa-right-left","fa-up-down","fa-arrow-trend-up","fa-arrow-trend-down","fa-arrow-pointer",
    "fa-diagram-project","fa-sitemap","fa-list","fa-list-check","fa-table","fa-table-cells",
    "fa-table-cells-large","fa-table-columns","fa-bars","fa-grip","fa-thumbtack","fa-tag",
    "fa-tags","fa-trash-can","fa-recycle",
    "fa-wrench","fa-screwdriver","fa-screwdriver-wrench","fa-hammer","fa-toolbox","fa-gear",
    "fa-gears","fa-sliders","fa-plug","fa-plug-circle-bolt","fa-battery-full","fa-battery-half",
    "fa-battery-quarter","fa-battery-empty",
    "fa-hands","fa-handshake","fa-hand-holding","fa-hand-holding-heart","fa-hands-holding",
    "fa-person","fa-person-walking","fa-person-running","fa-person-biking","fa-person-hiking",
    "fa-hand","fa-thumbs-up","fa-thumbs-down","fa-hand-spock","fa-hand-peace",
    "fa-cloud","fa-cloud-arrow-up","fa-cloud-arrow-down","fa-cloud-sun","fa-cloud-moon",
    "fa-cloud-rain","fa-cloud-bolt","fa-sun","fa-moon","fa-droplet","fa-water","fa-wind",
    "fa-snowflake","fa-fire-extinguisher","fa-bomb","fa-radiation","fa-biohazard",
    "fa-utensils","fa-mug-hot","fa-coffee","fa-wine-glass","fa-beer-mug-empty","fa-martini-glass",
    "fa-pizza-slice","fa-burger","fa-ice-cream","fa-cake-candles","fa-bowl-food","fa-wheat-awn",
    "fa-seedling","fa-leaf","fa-tree",
    "fa-paw","fa-dog","fa-cat","fa-fish","fa-hippo","fa-horse","fa-crow","fa-dove",
    "fa-feather-pointed","fa-frog","fa-otter","fa-shrimp","fa-worm",
    "fa-graduation-cap","fa-chalkboard","fa-book","fa-book-open","fa-bookmark","fa-newspaper",
    "fa-newspaper-check","fa-scroll","fa-feather","fa-pen","fa-pen-nib","fa-pencil","fa-marker",
    "fa-highlighter","fa-file-shield","fa-file-lines","fa-file-code","fa-file-image","fa-file-video",
    "fa-file-audio","fa-file-zipper","fa-file-csv","fa-file-excel","fa-file-word",
    "fa-file-powerpoint","fa-file-signature","fa-file-contract","fa-file-invoice","fa-file-pdf",
    "fa-folder","fa-folder-open","fa-folder-tree","fa-box-archive","fa-box","fa-cubes","fa-cube",
    "fa-calendar","fa-calendar-days","fa-calendar-check","fa-calendar-xmark","fa-calendar-plus",
    "fa-calendar-minus","fa-calendar-week",
    "fa-magnifying-glass","fa-magnifying-glass-chart","fa-magnifying-glass-dollar",
    "fa-magnifying-glass-location",
    "fa-circle-info","fa-circle-check","fa-circle-xmark","fa-circle-question",
    "fa-circle-exclamation","fa-circle-play","fa-circle-pause","fa-circle-stop","fa-circle-notch",
    "fa-circle-dot",
    "fa-instagram","fa-whatsapp","fa-facebook","fa-twitter","fa-x-twitter","fa-telegram",
    "fa-snapchat","fa-github","fa-youtube","fa-tiktok","fa-linkedin","fa-reddit","fa-discord",
    "fa-pinterest","fa-twitch","fa-weixin","fa-skype","fa-vk","fa-mastodon","fa-bluesky",
    "fa-threads","fa-android","fa-apple","fa-windows","fa-linux","fa-chrome","fa-firefox",
    "fa-edge","fa-safari","fa-python","fa-js","fa-node-js","fa-react","fa-vuejs","fa-angular",
    "fa-docker","fa-aws","fa-google","fa-microsoft","fa-php","fa-java","fa-rust","fa-golang",
    "fa-swift","fa-git-alt","fa-gitlab","fa-bitbucket","fa-npm","fa-yarn","fa-bitcoin",
    "fa-ethereum","fa-paypal","fa-stripe","fa-cc-visa","fa-cc-mastercard","fa-cc-amex",
    "fa-cc-paypal","fa-apple-pay","fa-google-pay","fa-amazon-pay","fa-d-and-d","fa-d-and-d-beyond",
    "fa-dungeon","fa-medium","fa-dev","fa-hacker-news","fa-stack-overflow","fa-slack","fa-figma",
    "fa-dribbble","fa-behance","fa-flickr","fa-vimeo","fa-soundcloud","fa-spotify",
]

PUBLIC_CATEGORIES = [
    ('Phone & Call','fa-phone',['number','number_adv','number_info','number_full','number_alt','num_operator','truecaller','truecaller_adv','num_loc']),
    ('Identity Suite','fa-id-card',['aadhar','aadhar_adv','adharfamily','adharfamily_adv','adharration','adharration_adv','aadhar_dob','aadhar_addr','voter','voter_adv']),
    ('Tax & PAN','fa-credit-card',['pan','pan_adv','pan_full','pan_dob','gst','gst_adv','gst_full','gst_verify']),
    ('Bank & UPI','fa-building-columns',['upi','upi_adv','upi_full','upi_bank','ifsc','ifsc_adv','ifsc_branch','ifsc_micr']),
    ('Email OSINT','fa-envelope',['email','email-lookup','email_adv','email_breach','email_gravatar']),
    ('Social Media','fa-share-nodes',['insta','insta_adv','insta_full','insta_email','git','git_adv','git_repo','tg','tg_adv','tg_info','snap','snap_adv','tw','tw_adv','fb','fb_adv','li','li_adv','yt']),
    ('Gaming','fa-gamepad',['ff','ff_adv','ff_full','bgmi','bgmi_adv','bgmi_full']),
    ('Network','fa-globe',['ip','ip_adv','ip_geo','whois']),
    ('Location','fa-location-dot',['pincode','pincode_adv']),
    ('Device / IMEI','fa-mobile-screen',['imei','imei_adv','imei_full']),
    ('Crypto','fa-bitcoin',['crypto','crypto_adv']),
    ('Leak / Breach','fa-database',['leak','leak_adv']),
    ('People Search','fa-user',['username','username_adv'])
]

KNOWN_PUBLIC_EP_KEYS = set()
for _, _, _lst in PUBLIC_CATEGORIES:
    KNOWN_PUBLIC_EP_KEYS.update(_lst)

def _default_db():
    db = {"api_keys": {}, "endpoints": {}, "resellers": {},
          "analytics": {"total_requests": 0, "today_calls": 0,
                        "today_date": str(date.today()), "api_usage": {}}}
    for api, meta in STANDARD_APIS.items():
        db["endpoints"][api] = {"url": "", "maintenance": False, "is_custom": False,
            "display_name": meta['name'], "param": meta['param'],
            "icon": normalize_icon(FA_DEFAULTS.get(api, 'fa-plug')), "hidden": False}
    return db

def ensure_ep_meta(db):
    changed = False
    if not isinstance(db.get("resellers"), dict):
        db["resellers"] = {}; changed = True
    for ep, d in db["endpoints"].items():
        if not isinstance(d, dict):
            db["endpoints"][ep] = d = {}; changed = True
        default = STANDARD_APIS.get(ep, {})
        for k, v in [('display_name', default.get('name', f'Custom: {ep}')),
                     ('param', default.get('param', 'query')),
                     ('icon', normalize_icon(FA_DEFAULTS.get(ep, 'fa-plug'))),
                     ('url', ''), ('maintenance', False),
                     ('is_custom', ep not in STANDARD_APIS), ('hidden', False)]:
            if k not in d: d[k] = v; changed = True
        fixed = normalize_icon(d.get('icon', 'fa-plug'))
        if fixed != d.get('icon'): d['icon'] = fixed; changed = True
    for rn, r in db["resellers"].items():
        if not isinstance(r, dict): continue
        if not isinstance(r.get("my_keys"), dict):
            r["my_keys"] = {}; changed = True
        if not isinstance(r.get("allowed_apis"), list):
            r["allowed_apis"] = []; changed = True
    if changed: save_db(db)
    return db

def load_db():
    if not os.path.exists(DB_FILE):
        db = _default_db(); save_db(db); return db
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f: data = json.load(f)
    except Exception:
        data = _default_db()
    if not isinstance(data.get("endpoints"), dict): data["endpoints"] = {}
    if not isinstance(data.get("api_keys"),  dict): data["api_keys"]  = {}
    if not isinstance(data.get("resellers"), dict): data["resellers"] = {}
    if not isinstance(data.get("analytics"), dict):
        data["analytics"] = {"total_requests": 0, "today_calls": 0,
                             "today_date": str(date.today()), "api_usage": {}}
    a = data["analytics"]
    a.setdefault("total_requests", 0); a.setdefault("today_calls", 0)
    a.setdefault("today_date", str(date.today())); a.setdefault("api_usage", {})
    for api, meta in STANDARD_APIS.items():
        if api not in data["endpoints"]:
            data["endpoints"][api] = {"url": "", "maintenance": False, "is_custom": False,
                "display_name": meta['name'], "param": meta['param'],
                "icon": normalize_icon(FA_DEFAULTS.get(api, 'fa-plug')), "hidden": False}
    return ensure_ep_meta(data)

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f: json.dump(data, f, indent=4)

def visible_endpoints(db):
    return {ep: d for ep, d in db["endpoints"].items() if not d.get("hidden")}

def get_keys_and_reset(db_data):
    today_str = str(date.today()); changed = False
    keys = db_data.get("api_keys", {})
    for k, v in keys.items():
        if v.get('last_used_date') != today_str:
            v['used'] = 0; v['last_used_date'] = today_str; changed = True
    if changed: save_db(db_data)
    return keys

def parse_expiry(s):
    if not s: return datetime(2099, 12, 31, 23, 59, 59)
    try:
        s = str(s)
        if len(s) == 10: return datetime.strptime(s, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    except Exception: return datetime(2099, 12, 31, 23, 59, 59)

def key_is_active(kv):
    if parse_expiry(kv.get('expiry_date')) <= datetime.now(): return False
    if kv.get('limit', 0) != 0 and kv.get('used', 0) >= kv.get('limit', 0): return False
    return True

def reseller_is_active(rs):
    if not rs.get('active', True): return False
    if parse_expiry(rs.get('expires_at')) <= datetime.now(): return False
    return True

def reseller_days_left(rs):
    try:
        exp = parse_expiry(rs.get('expires_at'))
        return max(0, (exp - datetime.now()).days)
    except Exception: return 0

def subkey_is_active(sk):
    return parse_expiry(sk.get('expires_at')) > datetime.now()

def bump_analytics(db, api_type):
    a = db["analytics"]
    a["total_requests"] = a.get("total_requests", 0) + 1
    today = str(date.today())
    if a.get("today_date") != today:
        a["today_date"] = today; a["today_calls"] = 0
    a["today_calls"] = a.get("today_calls", 0) + 1
    u = a.get("api_usage", {}); u[api_type] = u.get(api_type, 0) + 1; a["api_usage"] = u

RESTRICTED_WORDS = {'credit','owner','powered','buy','support','channel','telegram',
                    'author','created_by','api_by','developed_by','api_name','developer'}
def clean_response(data):
    if isinstance(data, dict):
        return {k: clean_response(v) for k, v in data.items() if k.lower() not in RESTRICTED_WORDS}
    if isinstance(data, list): return [clean_response(i) for i in data]
    return data

def gen_device_token():
    return secrets.token_urlsafe(32)

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.template_filter('icls')
def icls(icon):
    icon = normalize_icon(icon)
    return f"{fa_prefix(icon)} {icon}"

def admin_required(f):
    @wraps(f)
    def wrapper(*a, **kw):
        if not session.get('admin'): return redirect('/login')
        return f(*a, **kw)
    return wrapper

@app.errorhandler(Exception)
def handle_error(e):
    return f"<div style='background:#000;color:var(--red);padding:30px;font-family:sans-serif;min-height:100vh;'><h2>SERVER ERROR</h2><p>{e}</p><a href='/' style='color:var(--red-bright);'>Home</a></div>", 500

THEME_HEAD = """
<script>
(function(){
    var k = '{{ theme_key }}';
    var color = localStorage.getItem(k + '_color') || 'red';
    document.documentElement.setAttribute('data-theme', color);
    if(localStorage.getItem(k)==='light') document.documentElement.classList.add('light');
})();
</script>
"""

THEME_SCRIPT = """
<script>
function toggleTheme(){
    var html = document.documentElement;
    var k = '{{ theme_key }}';
    html.classList.toggle('light');
    localStorage.setItem(k, html.classList.contains('light') ? 'light' : 'dark');
    updateThemeIcons();
}
function setThemeColor(color){
    var k = '{{ theme_key }}';
    document.documentElement.setAttribute('data-theme', color);
    localStorage.setItem(k + '_color', color);
    document.querySelectorAll('.theme-dot').forEach(function(d){
        d.classList.toggle('active', d.dataset.color === color);
    });
}
function updateThemeIcons(){
    var light = document.documentElement.classList.contains('light');
    document.querySelectorAll('.theme-icon').forEach(function(el){
        el.className = light ? 'fas fa-moon theme-icon' : 'fas fa-sun theme-icon';
    });
    document.querySelectorAll('.theme-text').forEach(function(el){
        el.textContent = light ? 'NIGHT' : 'DAY';
    });
}
document.addEventListener('DOMContentLoaded', function(){
    updateThemeIcons();
    var cur = document.documentElement.getAttribute('data-theme') || 'red';
    document.querySelectorAll('.theme-dot').forEach(function(d){
        d.classList.toggle('active', d.dataset.color === cur);
    });
});
updateThemeIcons();
</script>
"""

THEME_VARS_CSS = """
:root{
    --bg:#000;
    --card:rgba(15,15,20,.55); --card2:rgba(20,20,26,.55); --card3:rgba(10,10,14,.78);
    --glass:rgba(255,255,255,.04); --glass-2:rgba(255,255,255,.06);
    --glass-border:rgba(255,255,255,.09);
    --text:#fff; --text-2:#ccc; --muted:#888; --muted-2:#666; --muted-3:#555;
    --border:rgba(255,255,255,.05); --border-2:rgba(255,255,255,.08);
    --input-bg:rgba(0,0,0,.55); --input-bg-2:rgba(0,0,0,.4);
    --grid-line:rgba(225,29,46,.035);
    
    --red-r:225; --red-g:29; --red-b:46;
    --red:#e11d2e; --red-bright:#ef4444; --red-deep:#7f1d1d;
    --red-glow:rgba(225,29,46,.15);
    --red-gradient:linear-gradient(135deg,#e11d2e,#991b1b);

    --maint:#ffa94d; --maint-glow:rgba(255,169,77,.15);
    --green:#10b981; --green-glow:rgba(16,185,129,.15);
    --purple:#8b5cf6; --purple-glow:rgba(139,92,246,.15);
    --shadow-card:0 20px 60px rgba(0,0,0,.9);
}
html[data-theme="blue"]{
    --red-r:37; --red-g:99; --red-b:235;
    --red:#2563eb; --red-bright:#3b82f6; --red-deep:#1e3a8a;
    --red-glow:rgba(37,99,235,.15);
    --red-gradient:linear-gradient(135deg,#2563eb,#1e40af);
}
html[data-theme="green"]{
    --red-r:5; --red-g:150; --red-b:105;
    --red:#059669; --red-bright:#10b981; --red-deep:#064e3b;
    --red-glow:rgba(5,150,105,.15);
    --red-gradient:linear-gradient(135deg,#10b981,#047857);
}
html[data-theme="orange"]{
    --red-r:234; --red-g:88; --red-b:12;
    --red:#ea580c; --red-bright:#f97316; --red-deep:#7c2d12;
    --red-glow:rgba(234,88,12,.15);
    --red-gradient:linear-gradient(135deg,#f97316,#c2410c);
}
html[data-theme="purple"]{
    --red-r:124; --red-g:58; --red-b:237;
    --red:#7c3aed; --red-bright:#8b5cf6; --red-deep:#4c1d95;
    --red-glow:rgba(124,58,237,.15);
    --red-gradient:linear-gradient(135deg,#8b5cf6,#6d28d9);
}
html.light{
    --bg:#f5f5f7;
    --card:rgba(255,255,255,.75); --card2:rgba(255,255,255,.85); --card3:rgba(255,255,255,.95);
    --glass:rgba(255,255,255,.55); --glass-2:rgba(255,255,255,.7);
    --glass-border:rgba(0,0,0,.08);
    --text:#0a0a0a; --text-2:#333; --muted:#666; --muted-2:#555; --muted-3:#888;
    --border:rgba(0,0,0,.08); --border-2:rgba(0,0,0,.12);
    --input-bg:rgba(255,255,255,.6); --input-bg-2:rgba(255,255,255,.7);
    --grid-line:rgba(225,29,46,.06);
    --shadow-card:0 20px 60px rgba(0,0,0,.1);
}

/* THEME COLOR DOTS */
.theme-dots{display:flex;justify-content:center;gap:10px;margin:14px 0 20px;}
.theme-dot{width:26px;height:26px;border-radius:50%;cursor:pointer;border:2px solid transparent;transition:.25s;position:relative;box-shadow:0 4px 10px rgba(0,0,0,.25);}
.theme-dot:hover{transform:scale(1.15);}
.theme-dot.active{border-color:#fff;box-shadow:0 0 0 2px rgba(255,255,255,.3),0 4px 12px rgba(0,0,0,.4);}
html.light .theme-dot.active{border-color:#111;box-shadow:0 0 0 2px rgba(0,0,0,.15),0 4px 12px rgba(0,0,0,.2);}
.theme-dot[data-color="red"]{background:#e11d2e;}
.theme-dot[data-color="blue"]{background:#2563eb;}
.theme-dot[data-color="green"]{background:#059669;}
.theme-dot[data-color="orange"]{background:#ea580c;}
.theme-dot[data-color="purple"]{background:#7c3aed;}
.theme-dot.active::after{content:'\\f00c';font-family:'Font Awesome 6 Free';font-weight:900;position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);color:#fff;font-size:10px;}

/* SIDEBAR THEME SECTION */
.sb-theme-sec { padding: 16px 10px 24px; }
.sb-theme-title { font-size: 10px; font-weight: 800; letter-spacing: 2px; color: var(--muted-3); margin-bottom: 12px; }
.sb-theme-dots { display: flex; gap: 10px; }
.sb-theme-dots .theme-dot { width: 22px; height: 22px; }
"""

ADMIN_TEMPLATE = """<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, viewport-fit=cover">
<title>Hindustan OSINT — Admin</title>
""" + THEME_HEAD + """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&display=swap');
""" + THEME_VARS_CSS + """
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent;}
html{scroll-behavior:smooth;}
html,body{overflow-x:hidden;}
body{background:var(--bg);color:var(--text);font-family:'Rajdhani',sans-serif;padding-bottom:80px;transition:background .25s,color .25s;}
body::after{content:'';position:fixed;inset:0;z-index:-1;pointer-events:none;background-image:radial-gradient(rgba(255,255,255,.03) 1px,transparent 1px);background-size:26px 26px;}
html.light body::after{background-image:radial-gradient(rgba(0,0,0,.03) 1px,transparent 1px);}
h1,h2,h3,.brand-name,.login-title,.unlock-btn{font-family:'Orbitron',sans-serif;}

.login-wrap{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px 18px;position:relative;}
.login-card{position:relative;z-index:2;width:100%;max-width:420px;padding:46px 26px 28px;border-radius:22px;background:var(--card);backdrop-filter:blur(26px) saturate(150%);border:1px solid var(--glass-border);box-shadow:0 20px 60px rgba(0,0,0,.2), inset 0 1px 0 rgba(255,255,255,.08), 0 0 80px var(--red-glow);animation:cardIn .55s cubic-bezier(.22,.9,.35,1.2) both;transition:box-shadow .3s;}
html.light .login-card{box-shadow:0 20px 60px rgba(0,0,0,.08), inset 0 1px 0 rgba(255,255,255,.7), 0 0 60px var(--red-glow);}
@keyframes cardIn{from{opacity:0;transform:translateY(24px) scale(.95);}to{opacity:1;transform:none;}}
.login-logo{width:84px;height:84px;margin:0 auto 20px;border-radius:20px;overflow:hidden;border:1px solid var(--glass-border);box-shadow:0 10px 40px var(--red-glow);}
.login-logo img{width:100%;height:100%;object-fit:cover;display:block;}
.login-title{text-align:center;font-size:21px;font-weight:900;letter-spacing:2.5px;margin-bottom:6px;}
.login-title .r{color:var(--red-bright);text-shadow:0 0 24px var(--red-glow);}
.login-sub{text-align:center;color:var(--muted-2);font-size:12px;letter-spacing:.5px;margin-bottom:26px;font-weight:500;}
.field{position:relative;margin-bottom:14px;}
.field .ficon{position:absolute;left:18px;top:50%;transform:translateY(-50%);color:var(--muted-3);font-size:15px;pointer-events:none;z-index:2;}
.field input{width:100%;padding:17px 48px 17px 48px;background:var(--input-bg-2);border:1px solid var(--glass-border);border-radius:12px;color:var(--text);font-family:inherit;font-size:15px;outline:none;transition:border-color .2s,box-shadow .2s;}
.field input::placeholder{color:var(--muted-3);}
.field input:focus{border-color:var(--red);box-shadow:0 0 0 3px var(--red-glow);}
.field .eye{position:absolute;right:16px;top:50%;transform:translateY(-50%);color:var(--muted-3);cursor:pointer;font-size:15px;z-index:3;padding:6px;}
.unlock-btn{width:100%;padding:16px;margin-top:12px;border:none;border-radius:12px;cursor:pointer;font-weight:900;font-size:13px;letter-spacing:3px;color:#fff;background:var(--red-gradient);box-shadow:0 8px 30px var(--red-glow);transition:transform .15s,background .3s,box-shadow .3s;display:flex;align-items:center;justify-content:center;gap:12px;font-family:'Orbitron',sans-serif;}
.unlock-btn:hover{transform:translateY(-2px);}
.unlock-btn i{font-size:14px;}
.error-msg{color:#ff6b6b;background:rgba(225,29,46,.1);padding:11px 14px;border-radius:10px;margin-bottom:16px;border:1px solid rgba(225,29,46,.35);font-weight:600;font-size:13px;text-align:center;display:flex;align-items:center;justify-content:center;gap:8px;}
.foot-note{text-align:center;margin-top:22px;color:var(--muted-3);font-size:10px;letter-spacing:4px;font-weight:700;text-transform:uppercase;}
.foot-note span{color:var(--red);}

.shell{display:flex;min-height:100vh;}
.sidebar{width:240px;background:var(--card3);backdrop-filter:blur(24px) saturate(150%);border-right:1px solid var(--glass-border);padding:18px 12px;position:fixed;top:0;left:0;height:100vh;height:100dvh;overflow-y:auto;z-index:60;display:flex;flex-direction:column;transition:transform .3s ease,background .25s;}
.brand{display:flex;align-items:center;gap:11px;padding:0 8px 16px;border-bottom:1px solid var(--border);margin-bottom:12px;}
.brand-logo{width:38px;height:38px;border-radius:10px;overflow:hidden;flex-shrink:0;border:1px solid var(--glass-border);}
.brand-logo img{width:100%;height:100%;object-fit:cover;display:block;}
.brand-text{display:flex;flex-direction:column;line-height:1.1;min-width:0;}
.brand-name{font-weight:700;letter-spacing:1.2px;font-size:12px;}
.brand-name .r{color:var(--red-bright);}
.brand-sub{color:var(--muted-3);font-size:9px;letter-spacing:1.5px;font-weight:600;margin-top:1px;}
.nav-label{color:var(--muted-3);font-size:10px;letter-spacing:2px;padding:12px 10px 6px;font-weight:700;}
.nav-item{display:flex;align-items:center;gap:12px;padding:11px 14px;border-radius:10px;color:var(--muted);text-decoration:none;font-weight:600;font-size:13.5px;cursor:pointer;transition:.2s;border:1px solid transparent;background:transparent;width:100%;text-align:left;font-family:inherit;}
.nav-item:hover{background:rgba(var(--red-r),var(--red-g),var(--red-b),.08);color:var(--text);border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.18);}
.nav-item.active{background:linear-gradient(90deg,var(--red-glow),transparent);color:var(--red-bright);border-left:3px solid var(--red);padding-left:11px;}
.nav-item i{width:18px;text-align:center;font-size:14px;}
.side-foot{margin-top:auto;}
.main{flex:1;margin-left:240px;padding:22px 24px 100px;min-width:0;}
.topbar-m{display:flex;align-items:center;justify-content:space-between;margin-bottom:22px;gap:12px;flex-wrap:wrap;}
.greet h1{font-size:22px;font-weight:700;} .greet p{color:var(--muted-2);font-size:12px;margin-top:3px;}
.top-actions{display:flex;gap:10px;align-items:center;flex-wrap:wrap;}
.search-box{background:var(--input-bg-2);border:1px solid var(--glass-border);border-radius:10px;padding:9px 14px;color:var(--text);font-family:inherit;font-size:13px;width:200px;outline:none;transition:.2s;}
.search-box::placeholder{color:var(--muted-3);}
.icon-btn{width:38px;height:38px;border-radius:10px;background:var(--input-bg-2);border:1px solid var(--glass-border);color:var(--muted);cursor:pointer;font-size:14px;display:flex;align-items:center;justify-content:center;text-decoration:none;transition:.2s;}
.icon-btn:hover{color:var(--red-bright);border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.5);}
.theme-round{height:38px;padding:0 14px;border-radius:10px;background:var(--input-bg-2);border:1px solid var(--glass-border);color:var(--muted);cursor:pointer;font-size:11px;font-family:'Orbitron',sans-serif;font-weight:700;letter-spacing:1.5px;display:inline-flex;align-items:center;justify-content:center;gap:7px;transition:.2s;text-transform:uppercase;}
.theme-round:hover{color:var(--red-bright);border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.5);}
.pill-btn{padding:9px 16px;border-radius:10px;background:var(--red-gradient);color:#fff;border:none;font-weight:700;font-family:inherit;font-size:13px;cursor:pointer;letter-spacing:.5px;display:inline-flex;align-items:center;gap:8px;justify-content:center;box-shadow:0 4px 14px rgba(var(--red-r),var(--red-g),var(--red-b),.35);transition:transform .15s;}
.pill-btn:hover{transform:translateY(-1px);}
.pill-btn i{font-size:12px;}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:24px;}
.stat{background:var(--card);backdrop-filter:blur(20px) saturate(140%);border:1px solid var(--glass-border);border-radius:14px;padding:18px;position:relative;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,.1), inset 0 1px 0 rgba(255,255,255,.05);}
.stat::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--red),transparent);opacity:.7;}
.stat .label{color:var(--muted-2);font-size:10px;letter-spacing:2px;font-weight:700;}
.stat .value{font-family:'Orbitron';font-size:30px;font-weight:700;margin-top:8px;line-height:1;}
.stat .delta{color:var(--red-bright);font-size:11px;margin-top:8px;font-weight:600;display:flex;align-items:center;gap:4px;}
.stat .corner{position:absolute;top:16px;right:16px;font-size:18px;color:var(--red);opacity:.85;}
.card{background:var(--card);backdrop-filter:blur(20px) saturate(140%);border:1px solid var(--glass-border);border-radius:16px;padding:20px;margin-bottom:22px;box-shadow:0 8px 32px rgba(0,0,0,.1), inset 0 1px 0 rgba(255,255,255,.05);}
.card-title{display:flex;align-items:center;gap:10px;font-size:15px;font-weight:700;margin-bottom:18px;}
.card-title i{color:var(--red-bright);font-size:15px;}
.card-title .hint{color:var(--muted-3);font-size:11px;margin-left:auto;letter-spacing:1px;font-weight:600;}
.form-label{color:var(--muted);font-size:11px;letter-spacing:2px;font-weight:700;margin:14px 0 8px;display:block;}
.form-control{width:100%;padding:12px 14px;background:var(--input-bg);border:1px solid var(--glass-border);color:var(--text);border-radius:10px;outline:none;font-family:inherit;font-size:14px;transition:.2s;}
.form-control::placeholder{color:var(--muted-3);}
.form-control:focus{border-color:var(--red);box-shadow:0 0 0 3px var(--red-glow);}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
@media(max-width:600px){.grid-2{grid-template-columns:1fr;}}
.icon-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(108px,1fr));gap:10px;max-height:340px;overflow-y:auto;padding:4px;}
.icon-grid::-webkit-scrollbar{width:6px;}
.icon-grid::-webkit-scrollbar-thumb{background:var(--red-glow);border-radius:3px;}
.icon-cell{background:var(--input-bg-2);border:1.5px solid var(--glass-border);border-radius:12px;padding:16px 6px 12px;text-align:center;cursor:pointer;transition:.2s;user-select:none;display:flex;flex-direction:column;align-items:center;gap:8px;}
.icon-cell:hover{border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.4);}
.icon-cell.selected{border-color:var(--red);background:var(--red-glow);}
.icon-cell .ico{font-size:20px;line-height:1;color:var(--muted-3);transition:.2s;}
.icon-cell.selected .ico{color:var(--red-bright);}
.icon-cell .nm{font-size:10px;font-weight:700;letter-spacing:1px;color:var(--muted-2);text-transform:uppercase;word-break:break-all;}
.icon-cell.selected .nm{color:var(--red-bright);}
.icon-cell input{display:none;}
.pill-group{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;}
.pill-opt{padding:14px 8px;border-radius:12px;border:1.5px solid var(--glass-border);background:var(--input-bg-2);text-align:center;cursor:pointer;transition:.2s;}
.pill-opt:hover{border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.4);}
.pill-opt.active{border-color:var(--red);background:var(--red-glow);}
.pill-opt .pt{font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center;gap:6px;color:var(--muted);}
.pill-opt.active .pt{color:var(--red-bright);}
.pill-opt .ps{font-size:10px;color:var(--muted-3);margin-top:4px;}
.tbl-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;}
table{width:100%;border-collapse:collapse;min-width:520px;}
th{text-align:left;padding:12px 10px;color:var(--muted-2);border-bottom:1px solid var(--border-2);font-size:10px;letter-spacing:2px;font-weight:700;}
td{padding:12px 10px;border-bottom:1px solid var(--border);font-size:13px;color:var(--text-2);}
.key-name{color:var(--red-bright);font-weight:700;font-family:'Share Tech Mono',monospace;word-break:break-all;}
.badge{display:inline-block;padding:3px 8px;border-radius:6px;font-size:10px;font-weight:700;letter-spacing:1px;}
.badge.on{background:var(--red-glow);color:var(--red-bright);border:1px solid rgba(var(--red-r),var(--red-g),var(--red-b),.4);}
.badge.off{background:rgba(120,120,120,.1);color:var(--muted);border:1px solid rgba(120,120,120,.3);}
.badge.custom{background:rgba(239,68,68,.15);color:#fca5a5;border:1px solid rgba(239,68,68,.4);}
.badge.maint{background:var(--maint-glow);color:var(--maint);border:1px solid rgba(255,169,77,.5);}
.badge.green{background:var(--green-glow);color:var(--green);border:1px solid rgba(16,185,129,.4);}
.badge.locked{background:rgba(99,102,241,.15);color:#a5b4fc;border:1px solid rgba(99,102,241,.4);}
.del-btn{background:var(--red-glow);border:1px solid rgba(var(--red-r),var(--red-g),var(--red-b),.4);color:var(--red-bright);padding:7px 11px;border-radius:8px;cursor:pointer;font-size:12px;font-family:inherit;}
.del-btn:hover{background:rgba(var(--red-r),var(--red-g),var(--red-b),.25);}
.edit-btn{background:var(--red-glow);border:1px solid rgba(var(--red-r),var(--red-g),var(--red-b),.4);color:var(--red-bright);padding:7px 11px;border-radius:8px;cursor:pointer;font-size:12px;margin-right:5px;font-family:inherit;}
.edit-btn:hover{background:rgba(var(--red-r),var(--red-g),var(--red-b),.25);}
.reset-btn{background:rgba(99,102,241,.15);border:1px solid rgba(99,102,241,.4);color:#a5b4fc;padding:7px 11px;border-radius:8px;cursor:pointer;font-size:12px;margin-right:5px;font-family:inherit;}
.reset-btn:hover{background:rgba(99,102,241,.25);}
.feat-row{background:var(--input-bg-2);padding:14px;border-radius:12px;border-left:3px solid var(--red);margin-bottom:10px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;}
.feat-row.maint{border-left-color:var(--maint);opacity:.85;}
.feat-ico{width:38px;height:38px;border-radius:9px;background:var(--red-glow);border:1px solid rgba(var(--red-r),var(--red-g),var(--red-b),.25);color:var(--red-bright);display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;}
.feat-meta{flex:1;min-width:160px;display:flex;flex-direction:column;gap:2px;}
.feat-name{font-weight:700;font-size:14px;}
.feat-ep{font-family:'Share Tech Mono',monospace;color:var(--red-bright);font-size:12px;}
.feat-param{color:var(--muted-2);font-size:11px;font-family:'Share Tech Mono',monospace;}
.feat-actions{display:flex;gap:6px;flex-shrink:0;}
.maint-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px;}
.maint-item{display:flex;align-items:center;gap:10px;background:var(--input-bg-2);border:1px solid var(--glass-border);border-radius:10px;padding:11px 12px;cursor:pointer;transition:.2s;}
.maint-item:hover{border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.4);}
.maint-item.on{border-color:var(--maint);background:var(--maint-glow);}
.maint-item i:first-child{color:var(--red-bright);font-size:14px;}
.maint-item.on i:first-child{color:var(--maint);}
.maint-name{font-size:12px;font-weight:700;font-family:'Share Tech Mono',monospace;flex:1;word-break:break-all;}
.maint-switch{width:36px;height:20px;border-radius:10px;background:rgba(120,120,120,.3);position:relative;flex-shrink:0;transition:.2s;}
.maint-item.on .maint-switch{background:var(--maint);}
.maint-switch::after{content:'';position:absolute;top:2px;left:2px;width:16px;height:16px;border-radius:50%;background:#fff;transition:.2s;}
.maint-item.on .maint-switch::after{left:18px;}
.maint-item input{display:none;}
.section{display:none;} .section.active{display:block;animation:fade .25s;}
@keyframes fade{from{opacity:0;transform:translateY(6px);}to{opacity:1;transform:none;}}
.modal-bg{display:none;position:fixed;inset:0;background:rgba(0,0,0,.85);backdrop-filter:blur(8px);z-index:200;align-items:center;justify-content:center;padding:20px;overflow-y:auto;}
.modal-bg.open{display:flex;}
.modal{background:var(--card2);backdrop-filter:blur(24px) saturate(150%);border:1px solid var(--glass-border);border-radius:18px;max-width:520px;width:100%;padding:26px 22px;box-shadow:var(--shadow-card),0 0 60px var(--red-glow);margin:auto;max-height:calc(100vh - 40px);overflow-y:auto;}
.modal h3{font-size:16px;color:var(--red-bright);margin-bottom:6px;letter-spacing:1px;display:flex;align-items:center;gap:10px;}
.modal .sub{color:var(--muted-2);font-size:12px;margin-bottom:20px;}
.modal .row{display:flex;gap:10px;margin-top:20px;}
.modal .row button{flex:1;padding:12px;border-radius:10px;font-family:inherit;font-weight:700;font-size:13px;cursor:pointer;border:none;}
.modal .cancel{background:var(--input-bg-2);color:var(--muted);border:1px solid var(--glass-border);}
.modal .save{background:var(--red-gradient);color:#fff;}
.modal .api-pick{max-height:200px;overflow-y:auto;border:1px solid var(--glass-border);border-radius:10px;padding:10px;background:var(--input-bg);margin-top:6px;}
.modal .api-pick label{display:flex;align-items:center;gap:8px;padding:7px 8px;border-radius:6px;font-size:13px;color:var(--text-2);cursor:pointer;}
.modal .api-pick label:hover{background:var(--red-glow);}
.modal .api-pick input{accent-color:var(--red);}
.icon-picker{display:grid;grid-template-columns:repeat(auto-fill,minmax(56px,1fr));gap:8px;max-height:230px;overflow-y:auto;padding:10px;background:var(--input-bg);border:1px solid var(--glass-border);border-radius:12px;margin-top:8px;}
.icon-picker::-webkit-scrollbar{width:6px;}
.icon-picker::-webkit-scrollbar-thumb{background:var(--red-glow);border-radius:3px;}
.icon-tile{aspect-ratio:1/1;border-radius:10px;background:var(--input-bg-2);border:1.5px solid var(--glass-border);color:var(--muted-2);display:flex;align-items:center;justify-content:center;font-size:17px;cursor:pointer;transition:.18s;user-select:none;}
.icon-tile:hover{border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.4);color:var(--text);}
.icon-tile.picked{border-color:var(--red);background:var(--red-glow);color:var(--red-bright);}
.icon-picker-search{width:100%;padding:9px 12px;background:var(--input-bg-2);border:1px solid var(--glass-border);border-radius:9px;color:var(--text);font-family:inherit;font-size:13px;outline:none;margin-top:6px;}
.icon-picker-search::placeholder{color:var(--muted-3);}
.auto-hint{font-size:10.5px;color:var(--muted-3);margin-top:6px;}
.auto-hint.active{color:var(--red-bright);}
.rslr-picker{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;max-height:280px;overflow-y:auto;padding:10px;background:var(--input-bg);border:1px solid var(--glass-border);border-radius:12px;margin-top:6px;}
.rslr-picker::-webkit-scrollbar{width:6px;}
.rslr-picker::-webkit-scrollbar-thumb{background:var(--red-glow);border-radius:3px;}
.rslr-item{display:flex;align-items:center;gap:8px;padding:9px 10px;border-radius:9px;background:var(--input-bg-2);border:1.5px solid var(--glass-border);cursor:pointer;transition:.15s;user-select:none;font-size:12px;font-weight:600;}
.rslr-item:hover{border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.4);}
.rslr-item.on{border-color:var(--red);background:var(--red-glow);}
.rslr-item i{font-size:12px;color:var(--muted-2);flex-shrink:0;}
.rslr-item.on i{color:var(--red-bright);}
.rslr-item span{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--muted);}
.rslr-item.on span{color:var(--red-bright);}
.rslr-item input{display:none;}
.rslr-toolbar{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap;}
.rslr-toolbar button{padding:7px 12px;border-radius:8px;background:var(--input-bg-2);border:1px solid var(--glass-border);color:var(--muted);font-family:inherit;font-size:11.5px;font-weight:700;cursor:pointer;}
.rslr-toolbar button:hover{color:var(--red-bright);border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.4);}
.mob-topbar{display:none;position:sticky;top:0;z-index:45;background:var(--card);backdrop-filter:blur(20px) saturate(150%);border-bottom:1px solid var(--glass-border);padding:11px 14px;align-items:center;justify-content:space-between;gap:10px;}
.mob-topbar .mt-left{display:flex;align-items:center;gap:10px;min-width:0;}
.mob-topbar .mt-logo{width:32px;height:32px;border-radius:9px;overflow:hidden;flex-shrink:0;border:1px solid var(--glass-border);}
.mob-topbar .mt-logo img{width:100%;height:100%;object-fit:cover;display:block;}
.mob-topbar .mt-title{font-family:'Orbitron',sans-serif;font-weight:700;font-size:12px;letter-spacing:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.mob-topbar .mt-title .r{color:var(--red-bright);}
.mob-burger{background:var(--input-bg-2);border:1px solid var(--glass-border);color:var(--text);font-size:15px;width:36px;height:36px;border-radius:9px;display:inline-flex;align-items:center;justify-content:center;cursor:pointer;}
.mob-burger:hover{color:var(--red-bright);border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.5);}
.sb-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.65);backdrop-filter:blur(4px);z-index:55;opacity:0;transition:opacity .3s;}
.sb-overlay.show{display:block;opacity:1;}
.mob-nav{position:fixed;bottom:0;left:0;right:0;background:var(--card3);backdrop-filter:blur(24px) saturate(150%);border-top:1px solid var(--glass-border);display:none;z-index:100;padding:8px 4px calc(8px + env(safe-area-inset-bottom));justify-content:space-around;}
.mob-tab{background:transparent;border:none;color:var(--muted-2);font-family:inherit;font-size:10px;display:flex;flex-direction:column;align-items:center;gap:4px;padding:8px 4px;border-radius:10px;cursor:pointer;flex:1;font-weight:700;}
.mob-tab i{font-size:17px;}
.mob-tab.active{color:var(--red-bright);background:var(--red-glow);}
@media(max-width:900px){
    .sidebar{background:var(--card3);box-shadow:8px 0 40px rgba(0,0,0,.65);height:100vh;height:100dvh;transform:translateX(-100%);width:250px;}
    html.light .sidebar{background:#ffffff;box-shadow:8px 0 40px rgba(0,0,0,.15);}
    .sidebar.open{transform:translateX(0);}
    body{padding-bottom:88px;}
    .main{margin-left:0;padding:14px 12px 100px;}
    .mob-topbar{display:flex;}
    .mob-nav{display:flex;}
    .stats{grid-template-columns:repeat(2,1fr);gap:10px;}
    .stat{padding:14px;border-radius:13px;}
    .stat .value{font-size:22px;}
    .topbar-m{display:none;}
    .card{padding:16px;border-radius:14px;margin-bottom:16px;}
    .grid-2{grid-template-columns:1fr;gap:10px;}
    .icon-grid{grid-template-columns:repeat(3,1fr);gap:8px;}
    .rslr-picker{grid-template-columns:repeat(2,1fr);}
    .tbl-wrap{margin:0 -12px;padding:0 12px;}
    table{min-width:440px;}
}
@media(max-width:520px){
    .stats{grid-template-columns:1fr 1fr;gap:8px;}
    .stat{padding:12px;border-radius:12px;}
    .stat .value{font-size:19px;}
    .icon-grid{grid-template-columns:repeat(2,1fr);gap:7px;}
    .rslr-picker{grid-template-columns:1fr;}
}
</style></head><body>

{% if not logged_in %}
<div class="login-wrap">
    <div class="login-card">
        <div class="login-logo"><img src="{{ banner_image }}" alt="Hindustan OSINT"></div>
        <div class="login-title">HINDUSTAN <span class="r">ADMIN</span></div>
        <div class="login-sub">Key Control Panel</div>
        
        {% if error_msg %}<div class="error-msg"><i class="fas fa-triangle-exclamation"></i> {{ error_msg }}</div>{% endif %}
        <form method="POST" action="/login" autocomplete="off">
            <div class="field">
                <input type="text" name="username" placeholder="Enter Admin Username" value="admin" autocomplete="off">
                <i class="fas fa-user ficon"></i>
            </div>
            <div class="field">
                <input type="password" name="password" id="adminPass" placeholder="Enter Admin Password" required autofocus>
                <i class="fas fa-lock ficon"></i>
                <i class="fas fa-eye eye" onclick="toggleEye()"></i>
            </div>
            <button type="submit" class="unlock-btn"><i class="fas fa-right-to-bracket"></i> LOGIN</button>
        </form>
        
        <div class="foot-note">Hindustan Hack <span>·</span> Cyber Security</div>
    </div>
</div>
<script>
function toggleEye(){
    const p = document.getElementById('adminPass');
    const e = document.querySelector('.eye');
    if(p.type === 'password'){ p.type = 'text'; e.classList.remove('fa-eye'); e.classList.add('fa-eye-slash'); }
    else { p.type = 'password'; e.classList.remove('fa-eye-slash'); e.classList.add('fa-eye'); }
}
</script>
{% else %}

<div class="sb-overlay" id="sbOverlay" onclick="closeAdminSidebar()"></div>

<div class="shell">
    <aside class="sidebar" id="adminSidebar">
        <div class="brand">
            <div class="brand-logo"><img src="{{ banner_image }}" alt="Logo"></div>
            <div class="brand-text"><span class="brand-name">HINDUSTAN <span class="r">OSINT</span></span><span class="brand-sub">CONTROL PANEL</span></div>
        </div>
        <div class="nav-label">MAIN</div>
        <button class="nav-item active" data-sec="dashboard" onclick="go('dashboard')"><i class="fas fa-table-cells-large"></i> Dashboard</button>
        <button class="nav-item" data-sec="keys" onclick="go('keys')"><i class="fas fa-key"></i> API Keys</button>
        <button class="nav-item" data-sec="resellers" onclick="go('resellers')"><i class="fas fa-users-gear"></i> Resellers</button>
        <button class="nav-item" data-sec="features" onclick="go('features')"><i class="fas fa-cubes"></i> Features</button>
        <button class="nav-item" data-sec="maintenance" onclick="go('maintenance')"><i class="fas fa-wrench"></i> Maintenance</button>
        <button class="nav-item" data-sec="security" onclick="go('security')"><i class="fas fa-shield-halved"></i> Security</button>
        <div class="nav-label">LINK</div>
        <a class="nav-item" href="/" target="_blank"><i class="fas fa-globe"></i> Public UI</a>
        <a class="nav-item" href="/reseller" target="_blank"><i class="fas fa-user-tie"></i> Reseller Login</a>
        <a class="nav-item" href="{{ tg_link }}" target="_blank"><i class="fab fa-telegram"></i> Channel</a>
        
        <div class="side-foot">
            <div class="sb-theme-sec">
                <div class="sb-theme-title">THEME COLORS</div>
                <div class="sb-theme-dots">
                    <div class="theme-dot" data-color="red" onclick="setThemeColor('red')"></div>
                    <div class="theme-dot" data-color="blue" onclick="setThemeColor('blue')"></div>
                    <div class="theme-dot" data-color="green" onclick="setThemeColor('green')"></div>
                    <div class="theme-dot" data-color="orange" onclick="setThemeColor('orange')"></div>
                    <div class="theme-dot" data-color="purple" onclick="setThemeColor('purple')"></div>
                </div>
            </div>
            <a class="nav-item" href="/logout" style="color:#ef4444;margin:8px 10px 0;"><i class="fas fa-power-off"></i> Logout</a>
        </div>
    </aside>

    <main class="main">
        <div class="mob-topbar">
            <div class="mt-left">
                <button class="mob-burger" onclick="openAdminSidebar()"><i class="fas fa-bars"></i></button>
                <div class="mt-logo"><img src="{{ banner_image }}" alt="Logo"></div>
                <div class="mt-title">HINDUSTAN <span class="r">OSINT</span></div>
            </div>
            <div style="display:flex;gap:8px;align-items:center;">
                <button class="mob-burger" onclick="toggleTheme()"><i class="fas fa-sun theme-icon"></i></button>
                <a href="/logout" class="mob-burger" style="color:#ef4444;"><i class="fas fa-power-off"></i></a>
            </div>
        </div>

        <div class="topbar-m">
            <div class="greet"><h1 id="greet-title">Good Morning, Admin</h1><p>Here's what's happening today.</p></div>
            <div class="top-actions">
                <input class="search-box" placeholder="Search...">
                <button class="theme-round" onclick="toggleTheme()"><i class="fas fa-sun theme-icon"></i> <span class="theme-text">DAY</span></button>
                <button class="icon-btn" onclick="location.reload()"><i class="fas fa-arrows-rotate"></i></button>
                <a href="/logout" class="icon-btn" style="color:#ef4444;"><i class="fas fa-power-off"></i></a>
            </div>
        </div>

        <section id="sec-dashboard" class="section active">
            <div class="stats">
                <div class="stat"><div class="corner"><i class="fas fa-key"></i></div>
                    <div class="label">TOTAL KEYS</div><div class="value">{{ total_keys }}</div>
                    <div class="delta"><i class="fas fa-arrow-up"></i> {{ active_keys }} active</div></div>
                <div class="stat"><div class="corner"><i class="fas fa-users-gear"></i></div>
                    <div class="label">RESELLERS</div><div class="value">{{ total_resellers }}</div>
                    <div class="delta"><i class="fas fa-circle"></i> {{ active_resellers }} active</div></div>
                <div class="stat"><div class="corner"><i class="fas fa-arrow-right"></i></div>
                    <div class="label">TOTAL CALLS</div><div class="value">{{ total_calls }}</div>
                    <div class="delta"><i class="fas fa-arrow-up"></i> {{ today_calls }} today</div></div>
                <div class="stat"><div class="corner"><i class="fas fa-calendar-day"></i></div>
                    <div class="label">TODAY</div><div class="value">{{ today_calls }}</div>
                    <div class="delta">{% if total_calls %}{{ (today_calls*100//total_calls) }}% of total{% else %}0%{% endif %}</div></div>
            </div>

            <div class="card">
                <div class="card-title"><i class="fas fa-plus"></i> Create API Key</div>
                <form method="POST" action="/generate">
                    <label class="form-label">API KEY</label>
                    <input type="text" name="key_name" class="form-control" placeholder="Enter unique API key" required>
                    <label class="form-label">ALLOWED APIS — TAP TO SELECT</label>
                    <div class="icon-grid">
                        {% for ep, d in endpoints.items() %}
                        <label class="icon-cell" data-api="{{ ep }}">
                            <input type="checkbox" name="allowed_apis" value="{{ ep }}">
                            <i class="{{ d.get('icon','fa-plug')|icls }} ico"></i>
                            <span class="nm">{{ ep }}</span>
                        </label>
                        {% endfor %}
                    </div>
                    <label class="form-label">DAILY LIMIT (0 = UNLIMITED)</label>
                    <input type="number" name="limit" class="form-control" value="100" min="0" required>
                    <label class="form-label">EXPIRY TYPE</label>
                    <div class="pill-group">
                        <div class="pill-opt active" data-mode="hours"><div class="pt"><i class="fas fa-clock"></i> Demo (Hours)</div><div class="ps">short-lived</div></div>
                        <div class="pill-opt" data-mode="days"><div class="pt"><i class="fas fa-gem"></i> Premium (Days)</div><div class="ps">standard</div></div>
                        <div class="pill-opt" data-mode="date"><div class="pt"><i class="fas fa-calendar"></i> Custom Date</div><div class="ps">pick</div></div>
                    </div>
                    <div id="inp-hours"><label class="form-label">HOURS</label><input type="number" name="hours" class="form-control" value="24" min="1"></div>
                    <div id="inp-days" style="display:none;"><label class="form-label">DAYS</label><input type="number" name="days" class="form-control" value="30" min="1"></div>
                    <div id="inp-date" style="display:none;"><label class="form-label">EXPIRY DATE</label><input type="date" name="expiry_date" class="form-control"></div>
                    <input type="hidden" name="expiry_mode" id="expiryMode" value="hours">
                    <button type="submit" class="pill-btn" style="margin-top:18px;padding:13px 20px;width:100%;">
                        <i class="fas fa-rocket"></i> Create Key
                    </button>
                </form>
            </div>

            <div class="card">
                <div class="card-title"><i class="fas fa-list"></i> All API Keys</div>
                <div class="tbl-wrap">
                    <table>
                        <tr><th>KEY</th><th>USAGE</th><th>EXPIRES</th><th>STATUS</th><th></th></tr>
                        {% if keys %}{% for k, v in keys.items() %}
                        <tr>
                            <td class="key-name">{{ k }}</td>
                            <td><span style="color:var(--red-bright);font-weight:700;">{{ v.used }}</span> / {% if v.limit == 0 %}∞{% else %}{{ v.limit }}{% endif %}</td>
                            <td style="font-size:11px;color:var(--muted);">{{ v.expiry_date }}</td>
                            <td>{% if key_active[k] %}<span class="badge on">ACTIVE</span>{% else %}<span class="badge off">OFF</span>{% endif %}</td>
                            <td style="text-align:right;white-space:nowrap;">
                                <button type="button" class="edit-btn"
                                    onclick='openKeyEdit({{ {"name":k,"limit":v.limit,"allowed":v.allowed_apis,"expiry":v.expiry_date}|tojson }})'>
                                    <i class="fas fa-pen"></i>
                                </button>
                                <form method="POST" action="/delete_key" style="margin:0;display:inline;">
                                    <input type="hidden" name="key_name" value="{{ k }}">
                                    <button type="submit" class="del-btn" onclick="return confirm('Delete {{ k }}?')"><i class="fas fa-trash"></i></button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}{% else %}
                        <tr><td colspan="5" style="text-align:center;color:var(--muted-2);padding:20px;">No keys yet.</td></tr>
                        {% endif %}
                    </table>
                </div>
            </div>
        </section>

        <section id="sec-keys" class="section">
            <div class="card">
                <div class="card-title"><i class="fas fa-key"></i> Active Keys</div>
                <div class="tbl-wrap">
                    <table>
                        <tr><th>KEY</th><th>USAGE</th><th>EXPIRES</th><th>STATUS</th><th></th></tr>
                        {% if keys %}{% for k, v in keys.items() %}
                        <tr>
                            <td class="key-name">{{ k }}</td>
                            <td><span style="color:var(--red-bright);font-weight:700;">{{ v.used }}</span> / {% if v.limit == 0 %}∞{% else %}{{ v.limit }}{% endif %}</td>
                            <td style="font-size:11px;color:var(--muted);">{{ v.expiry_date }}</td>
                            <td>{% if key_active[k] %}<span class="badge on">ACTIVE</span>{% else %}<span class="badge off">OFF</span>{% endif %}</td>
                            <td style="text-align:right;white-space:nowrap;">
                                <button type="button" class="edit-btn"
                                    onclick='openKeyEdit({{ {"name":k,"limit":v.limit,"allowed":v.allowed_apis,"expiry":v.expiry_date}|tojson }})'>
                                    <i class="fas fa-pen"></i>
                                </button>
                                <form method="POST" action="/delete_key" style="margin:0;display:inline;">
                                    <input type="hidden" name="key_name" value="{{ k }}">
                                    <button type="submit" class="del-btn"><i class="fas fa-trash"></i></button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}{% else %}
                        <tr><td colspan="5" style="text-align:center;color:var(--muted-2);padding:20px;">No keys.</td></tr>
                        {% endif %}
                    </table>
                </div>
            </div>
        </section>

        <section id="sec-resellers" class="section">
            <div class="card">
                <div class="card-title"><i class="fas fa-user-plus"></i> Create Reseller <span class="hint">name + features + days</span></div>
                <form method="POST" action="/add_reseller">
                    <div class="grid-2">
                        <div>
                            <label class="form-label">RESELLER NAME</label>
                            <input type="text" name="rslr_username" class="form-control" placeholder="e.g. john_doe" required pattern="[a-zA-Z0-9_.\\-]+" autocomplete="off">
                        </div>
                        <div>
                            <label class="form-label">PASSWORD</label>
                            <input type="text" name="rslr_password" class="form-control" placeholder="Set password" required autocomplete="off">
                        </div>
                    </div>
                    <div class="grid-2">
                        <div>
                            <label class="form-label">DURATION (DAYS)</label>
                            <input type="number" name="rslr_days" class="form-control" value="30" min="1" max="3650" required>
                        </div>
                        <div>
                            <label class="form-label">NOTES (optional)</label>
                            <input type="text" name="rslr_notes" class="form-control" placeholder="Optional info">
                        </div>
                    </div>
                    <label class="form-label">ALLOWED FEATURES — TAP TO SELECT</label>
                    <input type="text" class="icon-picker-search" id="rslrSearch" placeholder="Search feature...">
                    <div class="rslr-picker" id="rslrPicker">
                        {% for ep, d in endpoints.items() %}
                        <label class="rslr-item" data-name="{{ ep }} {{ d.get('display_name','') }}">
                            <input type="checkbox" name="rslr_features" value="{{ ep }}">
                            <i class="{{ d.get('icon','fa-plug')|icls }}"></i>
                            <span>{{ d.get('display_name', ep) }}</span>
                        </label>
                        {% endfor %}
                    </div>
                    <div class="rslr-toolbar">
                        <button type="button" onclick="rslrSelectAll(true)"><i class="fas fa-check-double"></i> Select All</button>
                        <button type="button" onclick="rslrSelectAll(false)"><i class="fas fa-xmark"></i> Clear</button>
                        <span style="margin-left:auto;font-size:11px;color:var(--muted-2);font-weight:700;align-self:center;"><span id="rslrCount">0</span> selected</span>
                    </div>
                    <button type="submit" class="pill-btn" style="margin-top:18px;padding:13px 20px;width:100%;">
                        <i class="fas fa-user-plus"></i> Create Reseller
                    </button>
                </form>
            </div>

            <div class="card">
                <div class="card-title"><i class="fas fa-users-gear"></i> All Resellers <span class="hint">{{ resellers|length }} total</span></div>
                <div class="tbl-wrap">
                    <table>
                        <tr><th>NAME</th><th>FEATURES</th><th>KEYS</th><th>DAYS LEFT</th><th>DEVICE</th><th>STATUS</th><th></th></tr>
                        {% if resellers %}{% for rn, r in resellers.items() %}
                        <tr>
                            <td class="key-name">{{ rn }}</td>
                            <td style="font-size:12px;">{{ r.allowed_apis|length }}</td>
                            <td style="font-size:12px;">{{ r.my_keys_count }}</td>
                            <td style="font-size:12px;color:{% if r.days_left <= 3 %}var(--red-bright){% elif r.days_left <= 7 %}var(--maint){% else %}var(--green){% endif %};font-weight:700;">{{ r.days_left }}d</td>
                            <td>{% if r.device_locked %}<span class="badge locked"><i class="fas fa-mobile-screen"></i> LOCK</span>{% else %}<span class="badge off">FREE</span>{% endif %}</td>
                            <td>{% if r.is_active %}<span class="badge green">ACTIVE</span>{% else %}<span class="badge off">EXPIRED</span>{% endif %}</td>
                            <td style="text-align:right;white-space:nowrap;">
                                <button type="button" class="edit-btn"
                                    onclick='openResellerEdit({{ {"name":rn,"password":r.password,"days":r.duration_days,"features":r.allowed_apis,"notes":r.notes}|tojson }})'>
                                    <i class="fas fa-pen"></i>
                                </button>
                                <form method="POST" action="/reset_reseller_device" style="margin:0;display:inline;" onsubmit="return confirm('Unlock device for {{ rn }}?');">
                                    <input type="hidden" name="rslr_username" value="{{ rn }}">
                                    <button type="submit" class="reset-btn" title="Unlock device"><i class="fas fa-mobile-screen-button"></i></button>
                                </form>
                                <form method="POST" action="/delete_reseller" style="margin:0;display:inline;" onsubmit="return confirm('Delete reseller {{ rn }}?');">
                                    <input type="hidden" name="rslr_username" value="{{ rn }}">
                                    <button type="submit" class="del-btn"><i class="fas fa-trash"></i></button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}{% else %}
                        <tr><td colspan="7" style="text-align:center;color:var(--muted-2);padding:20px;">No resellers yet.</td></tr>
                        {% endif %}
                    </table>
                </div>
            </div>
        </section>

        <section id="sec-features" class="section">
            <div class="card">
                <div class="card-title"><i class="fas fa-plus-circle"></i> Add New Feature <span class="hint">icon auto-detect</span></div>
                <form method="POST" action="/add_feature" id="addFeatForm">
                    <div class="grid-2">
                        <div>
                            <label class="form-label">ENDPOINT NAME</label>
                            <input type="text" name="ep_name" id="newEpName" class="form-control" placeholder="e.g. instagram" required pattern="[a-zA-Z0-9_\\-]+" autocomplete="off">
                        </div>
                        <div>
                            <label class="form-label">DISPLAY NAME</label>
                            <input type="text" name="ep_display" id="newEpDisplay" class="form-control" placeholder="e.g. Instagram Lookup" required autocomplete="off">
                        </div>
                    </div>
                    <div class="grid-2">
                        <div>
                            <label class="form-label">PARAM NAME</label>
                            <input type="text" name="ep_param" class="form-control" placeholder="e.g. username, num" required pattern="[a-zA-Z0-9_]+">
                        </div>
                        <div>
                            <label class="form-label">SELECTED ICON</label>
                            <div class="icon-pick">
                                <div class="icon-preview" id="newIconPreview"><i class="fas fa-plug"></i></div>
                                <input type="text" name="ep_icon" id="newIconInput" class="form-control" placeholder="fa-plug" required readonly style="cursor:default;font-family:ui-monospace,monospace;font-size:12.5px;">
                            </div>
                            <div class="auto-hint" id="autoHint">Icon auto-select</div>
                        </div>
                    </div>
                    <label class="form-label">PICK ICON — TAP TO SELECT</label>
                    <input type="text" class="icon-picker-search" id="iconSearch" placeholder="Search icon...">
                    <div class="icon-picker" id="iconPicker">
                        {% for ic in icon_choices %}
                        <div class="icon-tile" data-icon="{{ ic }}" title="{{ ic }}"><i class="{{ ic|icls }}"></i></div>
                        {% endfor %}
                    </div>
                    <label class="form-label">BACKEND URL (optional)</label>
                    <input type="url" name="ep_url" class="form-control" placeholder="https://backend.example.com/api?num=">
                    <label class="form-label" style="display:flex;align-items:center;gap:8px;cursor:pointer;text-transform:none;letter-spacing:0;">
                        <input type="checkbox" name="ep_maint" style="width:18px;height:18px;accent-color:var(--red);">
                        Start in Maintenance mode
                    </label>
                    <button type="submit" class="pill-btn" style="margin-top:18px;padding:13px 20px;width:100%;">
                        <i class="fas fa-cubes"></i> Add Feature
                    </button>
                </form>
            </div>

            <div class="card">
                <div class="card-title"><i class="fas fa-cubes"></i> All Features <span class="hint">{{ endpoints|length }} total</span></div>
                {% for ep, d in endpoints.items() %}
                {% set is_m = d.get('maintenance') %}
                <div class="feat-row {% if is_m %}maint{% endif %}">
                    <div class="feat-ico"><i class="{{ d.get('icon','fa-plug')|icls }}"></i></div>
                    <div class="feat-meta">
                        <div class="feat-name">{{ d.get('display_name', ep) }}
                            {% if is_m %}<span class="badge maint" style="margin-left:6px;font-size:9px;">MAINT</span>{% endif %}
                            {% if d.get('is_custom') %}<span class="badge custom" style="margin-left:6px;font-size:9px;">CUSTOM</span>{% endif %}
                        </div>
                        <div class="feat-ep">/{{ ep }}</div>
                        <div class="feat-param">?{{ d.get('param','query') }}=VALUE</div>
                    </div>
                    <div class="feat-actions">
                        <button type="button" class="edit-btn"
                            onclick='openFeatEdit({{ {"ep":ep,"display":d.get("display_name",ep),"param":d.get("param","query"),"icon":d.get("icon","fa-plug"),"url":d.get("url",""),"maint":is_m}|tojson }})'>
                            <i class="fas fa-pen"></i>
                        </button>
                        <form method="POST" action="/delete_feature" style="margin:0;display:inline;" onsubmit="return confirm('Delete /{{ ep }}?');">
                            <input type="hidden" name="ep_name" value="{{ ep }}">
                            <button type="submit" class="del-btn"><i class="fas fa-trash"></i></button>
                        </form>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>

        <section id="sec-maintenance" class="section">
            <div class="card">
                <div class="card-title"><i class="fas fa-wrench"></i> Maintenance Control <span class="hint">tap + save</span></div>
                <form method="POST" action="/save_maintenance">
                    <div class="maint-grid">
                        {% for ep, d in endpoints.items() %}
                        <label class="maint-item {% if d.get('maintenance') %}on{% endif %}">
                            <input type="checkbox" name="maint_{{ ep }}" {% if d.get('maintenance') %}checked{% endif %}>
                            <i class="{{ d.get('icon','fa-plug')|icls }}"></i>
                            <span class="maint-name">{{ ep }}</span>
                            <span class="maint-switch"></span>
                        </label>
                        {% endfor %}
                    </div>
                    <button type="submit" class="pill-btn" style="margin-top:16px;padding:13px 20px;width:100%;">
                        <i class="fas fa-floppy-disk"></i> Save Maintenance
                    </button>
                </form>
            </div>
        </section>

        <section id="sec-security" class="section">
            <div class="card">
                <div class="card-title"><i class="fas fa-shield-halved"></i> Security & Settings</div>
                <form method="POST" action="/change_password">
                    <label class="form-label">CURRENT PASSWORD</label>
                    <input type="password" name="old_pass" class="form-control" required>
                    <label class="form-label">SECRET AUTH KEY</label>
                    <input type="password" name="auth_key" class="form-control" required>
                    <label class="form-label">NEW PASSWORD</label>
                    <input type="password" name="new_pass" class="form-control" required>
                    <button type="submit" class="pill-btn" style="width:100%;margin-top:16px;padding:13px;">UPDATE</button>
                </form>
            </div>
        </section>
    </main>
</div>

<div class="modal-bg" id="keyModal">
    <div class="modal">
        <h3><i class="fas fa-pen-to-square"></i> Change API Key</h3>
        <div class="sub">Rename, change limit or expiry.</div>
        <form method="POST" action="/edit_key">
            <label class="form-label">NEW KEY NAME</label>
            <input type="text" name="new_name" id="kName" class="form-control" required autocomplete="off">
            <label class="form-label">DAILY LIMIT (0 = UNLIMITED)</label>
            <input type="number" name="new_limit" id="kLimit" class="form-control" min="0" required>
            <label class="form-label">EXPIRY (YYYY-MM-DD HH:MM:SS)</label>
            <input type="text" name="new_expiry" id="kExpiry" class="form-control" required>
            <label class="form-label">ALLOWED APIS</label>
            <div class="api-pick" id="kApis">
                {% for ep, d in endpoints.items() %}
                <label><input type="checkbox" name="new_allowed" value="{{ ep }}"> <i class="{{ d.get('icon','fa-plug')|icls }}" style="color:var(--red-bright);font-size:11px;"></i> {{ ep }}</label>
                {% endfor %}
            </div>
            <input type="hidden" name="old_name" id="kOld">
            <div class="row">
                <button type="button" class="cancel" onclick="closeKeyEdit()">Cancel</button>
                <button type="submit" class="save"><i class="fas fa-check"></i> Save</button>
            </div>
        </form>
    </div>
</div>

<div class="modal-bg" id="featModal">
    <div class="modal">
        <h3><i class="fas fa-pen-to-square"></i> Edit Feature</h3>
        <div class="sub">Update feature details.</div>
        <form method="POST" action="/edit_feature">
            <label class="form-label">ENDPOINT ROUTE</label>
            <input type="text" name="new_ep" id="fEp" class="form-control" required pattern="[a-zA-Z0-9_\\-]+">
            <label class="form-label">DISPLAY NAME</label>
            <input type="text" name="new_display" id="fDisplay" class="form-control" required>
            <div class="grid-2">
                <div>
                    <label class="form-label">PARAM NAME</label>
                    <input type="text" name="new_param" id="fParam" class="form-control" required pattern="[a-zA-Z0-9_]+">
                </div>
                <div>
                    <label class="form-label">ICON</label>
                    <div class="icon-pick">
                        <div class="icon-preview" id="fIconPreview"><i class="fas fa-plug"></i></div>
                        <input type="text" name="new_icon" id="fIcon" class="form-control" placeholder="fa-plug">
                    </div>
                </div>
            </div>
            <label class="form-label">QUICK PICK ICON</label>
            <div class="icon-picker" id="featIconPicker">
                {% for ic in icon_choices %}
                <div class="icon-tile" data-icon="{{ ic }}" title="{{ ic }}" data-target="fIcon"><i class="{{ ic|icls }}"></i></div>
                {% endfor %}
            </div>
            <label class="form-label">BACKEND URL</label>
            <input type="url" name="new_url" id="fUrl" class="form-control" placeholder="https://backend.example.com/api?num=">
            <label class="form-label" style="display:flex;align-items:center;gap:8px;cursor:pointer;text-transform:none;letter-spacing:0;">
                <input type="checkbox" name="new_maint" id="fMaint" style="width:18px;height:18px;accent-color:var(--red);">
                Set to Maintenance mode
            </label>
            <input type="hidden" name="old_ep" id="fOld">
            <div class="row">
                <button type="button" class="cancel" onclick="closeFeatEdit()">Cancel</button>
                <button type="submit" class="save"><i class="fas fa-check"></i> Save Changes</button>
            </div>
        </form>
    </div>
</div>

<div class="modal-bg" id="rslrModal">
    <div class="modal">
        <h3><i class="fas fa-user-pen"></i> Edit Reseller</h3>
        <div class="sub">Update password, duration, features.</div>
        <form method="POST" action="/edit_reseller">
            <label class="form-label">USERNAME</label>
            <input type="text" name="rslr_new_username" id="rName" class="form-control" required pattern="[a-zA-Z0-9_.\\-]+">
            <label class="form-label">PASSWORD</label>
            <input type="text" name="rslr_new_password" id="rPass" class="form-control" required>
            <label class="form-label">DURATION (DAYS FROM NOW)</label>
            <input type="number" name="rslr_new_days" id="rDays" class="form-control" min="1" max="3650" required>
            <label class="form-label">NOTES</label>
            <input type="text" name="rslr_new_notes" id="rNotes" class="form-control" placeholder="Optional">
            <label class="form-label">ALLOWED FEATURES</label>
            <input type="text" class="icon-picker-search" id="rSearch" placeholder="Search feature...">
            <div class="rslr-picker" id="rPicker" style="max-height:220px;">
                {% for ep, d in endpoints.items() %}
                <label class="rslr-item" data-name="{{ ep }} {{ d.get('display_name','') }}">
                    <input type="checkbox" name="rslr_new_features" value="{{ ep }}">
                    <i class="{{ d.get('icon','fa-plug')|icls }}"></i>
                    <span>{{ d.get('display_name', ep) }}</span>
                </label>
                {% endfor %}
            </div>
            <div class="rslr-toolbar">
                <button type="button" onclick="rSelectAll(true)"><i class="fas fa-check-double"></i> All</button>
                <button type="button" onclick="rSelectAll(false)"><i class="fas fa-xmark"></i> Clear</button>
                <span style="margin-left:auto;font-size:11px;color:var(--muted-2);font-weight:700;align-self:center;"><span id="rCount">0</span> selected</span>
            </div>
            <input type="hidden" name="rslr_old_username" id="rOld">
            <div class="row">
                <button type="button" class="cancel" onclick="closeResellerEdit()">Cancel</button>
                <button type="submit" class="save"><i class="fas fa-check"></i> Save</button>
            </div>
        </form>
    </div>
</div>

<nav class="mob-nav">
    <button class="mob-tab active" data-sec="dashboard" onclick="go('dashboard')"><i class="fas fa-table-cells-large"></i>Dash</button>
    <button class="mob-tab" data-sec="keys" onclick="go('keys')"><i class="fas fa-key"></i>Keys</button>
    <button class="mob-tab" data-sec="resellers" onclick="go('resellers')"><i class="fas fa-users-gear"></i>Resel</button>
    <button class="mob-tab" data-sec="features" onclick="go('features')"><i class="fas fa-cubes"></i>Feat</button>
    <button class="mob-tab" data-sec="security" onclick="go('security')"><i class="fas fa-shield-halved"></i>Sec</button>
</nav>

<script>
var BRAND_ICONS = {{ brand_icons|tojson }};
function faPrefix(icon){ if(!icon) return 'fas'; return BRAND_ICONS.indexOf(icon) !== -1 ? 'fab' : 'fas'; }
function renderIcon(icon){ if(!icon) icon = 'fa-plug'; return '<i class="' + faPrefix(icon) + ' ' + icon + '"></i>'; }
var AUTO_ICONS = {{ auto_icons_json|safe }};
var AUTO_KEYS_SORTED = Object.keys(AUTO_ICONS).sort(function(a,b){return b.length - a.length;});
function autoIcon(name){
    if(!name) return null;
    var n = String(name).toLowerCase().replace(/[-_ ]/g,'');
    if(AUTO_ICONS[n]) return AUTO_ICONS[n];
    for(var i=0;i<AUTO_KEYS_SORTED.length;i++){
        var kw = AUTO_KEYS_SORTED[i];
        if(n.indexOf(kw) !== -1) return AUTO_ICONS[kw];
    }
    return null;
}
function openAdminSidebar(){document.getElementById('adminSidebar').classList.add('open');document.getElementById('sbOverlay').classList.add('show');document.body.style.overflow='hidden';}
function closeAdminSidebar(){document.getElementById('adminSidebar').classList.remove('open');document.getElementById('sbOverlay').classList.remove('show');document.body.style.overflow='';}
window.addEventListener('resize', function(){ if(window.innerWidth > 900) closeAdminSidebar(); });
function go(id){
    document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));
    document.querySelectorAll('.nav-item[data-sec]').forEach(n=>n.classList.remove('active'));
    document.querySelectorAll('.mob-tab').forEach(n=>n.classList.remove('active'));
    var sec = document.getElementById('sec-'+id); if(sec) sec.classList.add('active');
    document.querySelectorAll('[data-sec="'+id+'"]').forEach(n=>n.classList.add('active'));
    closeAdminSidebar();
    window.scrollTo({top:0,behavior:'smooth'});
}
document.querySelectorAll('.icon-cell[data-api]').forEach(cell=>{
    cell.addEventListener('click', e=>{
        e.preventDefault();
        const cb = cell.querySelector('input');
        cb.checked = !cb.checked;
        cell.classList.toggle('selected', cb.checked);
    });
});
document.querySelectorAll('.pill-opt').forEach(p=>{
    p.addEventListener('click', ()=>{
        document.querySelectorAll('.pill-opt').forEach(x=>x.classList.remove('active'));
        p.classList.add('active');
        const m = p.dataset.mode;
        document.getElementById('expiryMode').value = m;
        document.getElementById('inp-hours').style.display = m==='hours'?'block':'none';
        document.getElementById('inp-days').style.display  = m==='days' ?'block':'none';
        document.getElementById('inp-date').style.display  = m==='date' ?'block':'none';
    });
});
document.querySelectorAll('.maint-item').forEach(item=>{
    item.addEventListener('click', e=>{
        e.preventDefault();
        const cb = item.querySelector('input[type=checkbox]');
        cb.checked = !cb.checked;
        item.classList.toggle('on', cb.checked);
    });
});
function bindRslrPicker(pickerId, searchId, countId){
    var picker = document.getElementById(pickerId);
    var search = document.getElementById(searchId);
    var count = document.getElementById(countId);
    function refreshCount(){ if(count && picker) count.textContent = picker.querySelectorAll('input[type=checkbox]:checked').length; }
    if(picker){
        picker.querySelectorAll('.rslr-item').forEach(function(item){
            item.addEventListener('click', function(e){
                e.preventDefault();
                var cb = item.querySelector('input');
                cb.checked = !cb.checked;
                item.classList.toggle('on', cb.checked);
                refreshCount();
            });
        });
    }
    if(search && picker){
        search.addEventListener('input', function(){
            var q = this.value.trim().toLowerCase();
            picker.querySelectorAll('.rslr-item').forEach(function(item){
                var n = (item.dataset.name || '').toLowerCase();
                item.style.display = (!q || n.indexOf(q) !== -1) ? '' : 'none';
            });
        });
    }
    refreshCount();
}
bindRslrPicker('rslrPicker','rslrSearch','rslrCount');
bindRslrPicker('rPicker','rSearch','rCount');
function rslrSelectAll(on){
    var p = document.getElementById('rslrPicker');
    p.querySelectorAll('.rslr-item').forEach(function(item){
        if(item.style.display === 'none') return;
        var cb = item.querySelector('input'); cb.checked = on; item.classList.toggle('on', on);
    });
    document.getElementById('rslrCount').textContent = p.querySelectorAll('input[type=checkbox]:checked').length;
}
function rSelectAll(on){
    var p = document.getElementById('rPicker');
    p.querySelectorAll('.rslr-item').forEach(function(item){
        var cb = item.querySelector('input'); cb.checked = on; item.classList.toggle('on', on);
    });
    document.getElementById('rCount').textContent = p.querySelectorAll('input[type=checkbox]:checked').length;
}
var newEpName = document.getElementById('newEpName');
var newEpDisplay = document.getElementById('newEpDisplay');
var newIconInput = document.getElementById('newIconInput');
var newIconPreview = document.getElementById('newIconPreview');
var autoHint = document.getElementById('autoHint');
var userPickedIcon = false;
function refreshPreview(){ if(newIconPreview && newIconInput) newIconPreview.innerHTML = renderIcon(newIconInput.value || 'fa-plug'); }
function tryAutoIcon(){
    if(userPickedIcon || !newEpName) return;
    var hit = autoIcon(newEpName.value) || autoIcon(newEpDisplay.value);
    if(hit){ newIconInput.value = hit; refreshPreview(); if(autoHint){autoHint.textContent='Auto: '+hit;autoHint.classList.add('active');} }
}
if(newEpName) newEpName.addEventListener('input', tryAutoIcon);
if(newEpDisplay) newEpDisplay.addEventListener('input', tryAutoIcon);
document.querySelectorAll('#iconPicker .icon-tile').forEach(function(tile){
    tile.addEventListener('click', function(){
        document.querySelectorAll('#iconPicker .icon-tile').forEach(t=>t.classList.remove('picked'));
        tile.classList.add('picked');
        newIconInput.value = tile.dataset.icon; userPickedIcon = true;
        refreshPreview(); if(autoHint){autoHint.textContent='Picked: '+tile.dataset.icon;autoHint.classList.add('active');}
    });
});
var iconSearch = document.getElementById('iconSearch');
if(iconSearch){
    iconSearch.addEventListener('input', function(){
        var q = this.value.trim().toLowerCase();
        document.querySelectorAll('#iconPicker .icon-tile').forEach(function(t){
            t.style.display = (!q || t.dataset.icon.toLowerCase().indexOf(q) !== -1) ? '' : 'none';
        });
    });
}
var fIcon = document.getElementById('fIcon');
var fIconPreview = document.getElementById('fIconPreview');
if(fIcon){ fIcon.addEventListener('input', function(){ fIconPreview.innerHTML = renderIcon(fIcon.value); }); }
document.querySelectorAll('#featIconPicker .icon-tile').forEach(function(tile){
    tile.addEventListener('click', function(){
        document.querySelectorAll('#featIconPicker .icon-tile').forEach(t=>t.classList.remove('picked'));
        tile.classList.add('picked');
        var target = document.getElementById(tile.dataset.target);
        if(target){ target.value = tile.dataset.icon; target.dispatchEvent(new Event('input')); }
    });
});
function openKeyEdit(data){
    document.getElementById('kOld').value = data.name;
    document.getElementById('kName').value = data.name;
    document.getElementById('kLimit').value = data.limit;
    document.getElementById('kExpiry').value = data.expiry;
    document.querySelectorAll('#kApis input[type=checkbox]').forEach(b => b.checked = (data.allowed||[]).includes(b.value));
    document.getElementById('keyModal').classList.add('open');
}
function closeKeyEdit(){ document.getElementById('keyModal').classList.remove('open'); }
document.getElementById('keyModal').addEventListener('click', e => { if(e.target.id === 'keyModal') closeKeyEdit(); });
function openFeatEdit(data){
    document.getElementById('fOld').value = data.ep;
    document.getElementById('fEp').value = data.ep;
    document.getElementById('fDisplay').value = data.display;
    document.getElementById('fParam').value = data.param;
    fIcon.value = data.icon;
    fIconPreview.innerHTML = renderIcon(data.icon);
    document.getElementById('fUrl').value = data.url || '';
    document.getElementById('fMaint').checked = !!data.maint;
    document.querySelectorAll('#featIconPicker .icon-tile').forEach(function(t){
        t.classList.toggle('picked', t.dataset.icon === data.icon);
    });
    document.getElementById('featModal').classList.add('open');
}
function closeFeatEdit(){ document.getElementById('featModal').classList.remove('open'); }
document.getElementById('featModal').addEventListener('click', e => { if(e.target.id === 'featModal') closeFeatEdit(); });
function openResellerEdit(data){
    document.getElementById('rOld').value = data.name;
    document.getElementById('rName').value = data.name;
    document.getElementById('rPass').value = data.password;
    document.getElementById('rDays').value = data.days;
    document.getElementById('rNotes').value = data.notes || '';
    var picker = document.getElementById('rPicker');
    picker.querySelectorAll('.rslr-item').forEach(function(item){
        var cb = item.querySelector('input');
        var on = (data.features || []).indexOf(cb.value) !== -1;
        cb.checked = on; item.classList.toggle('on', on);
    });
    document.getElementById('rCount').textContent = picker.querySelectorAll('input[type=checkbox]:checked').length;
    document.getElementById('rslrModal').classList.add('open');
}
function closeResellerEdit(){ document.getElementById('rslrModal').classList.remove('open'); }
document.getElementById('rslrModal').addEventListener('click', e => { if(e.target.id === 'rslrModal') closeResellerEdit(); });
(function(){
    const h = new Date().getHours();
    const g = h<12?'Good Morning':h<17?'Good Afternoon':h<21?'Good Evening':'Good Night';
    const el = document.getElementById('greet-title');
    if(el) el.textContent = g + ', Admin';
})();
</script>
{% endif %}
""" + THEME_SCRIPT + """
</body></html>"""

# ============================================================
# PUBLIC LOGIN TEMPLATE
# ============================================================
PUBLIC_LOGIN_TEMPLATE = """<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, viewport-fit=cover">
<title>Hindustan OSINT — Sign In</title>
""" + THEME_HEAD + """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
""" + THEME_VARS_CSS + """
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent;}
html,body{overflow-x:hidden;}
body{background:var(--bg);color:var(--text);font-family:'Inter',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;transition:background .25s,color .25s;}
.login-card{position:relative;z-index:2;width:100%;max-width:430px;padding:46px 28px 30px;border-radius:22px;background:var(--card);backdrop-filter:blur(26px) saturate(150%);border:1px solid var(--glass-border);box-shadow:0 20px 60px rgba(0,0,0,.2), inset 0 1px 0 rgba(255,255,255,.08), 0 0 80px var(--red-glow);animation:cardIn .55s cubic-bezier(.22,.9,.35,1.2) both;transition:box-shadow .3s;}
html.light .login-card{box-shadow:0 20px 60px rgba(0,0,0,.08), inset 0 1px 0 rgba(255,255,255,.7), 0 0 60px var(--red-glow);}
@keyframes cardIn{from{opacity:0;transform:translateY(24px) scale(.95);}to{opacity:1;transform:none;}}
.head{display:flex;flex-direction:column;align-items:center;margin-bottom:4px;}
.login-logo{width:80px;height:80px;border-radius:20px;overflow:hidden;border:1px solid var(--glass-border);box-shadow:0 12px 40px var(--red-glow);margin-bottom:14px;}
.login-logo img{width:100%;height:100%;object-fit:cover;display:block;}
.login-title{text-align:center;font-size:22px;font-weight:900;letter-spacing:1.2px;margin-bottom:4px;}
.login-title .r{color:var(--red-bright);transition:color .3s;text-shadow:0 0 24px var(--red-glow);}
.login-sub{text-align:center;color:var(--muted-2);font-size:12.5px;font-weight:500;margin-bottom:26px;}
.field{position:relative;margin-bottom:14px;}
.field .ficon{position:absolute;left:18px;top:50%;transform:translateY(-50%);color:var(--muted-3);font-size:15px;pointer-events:none;z-index:2;transition:color .2s;}
.field input{width:100%;padding:17px 48px 17px 48px;background:var(--input-bg-2);border:1px solid var(--glass-border);border-radius:12px;color:var(--text);font-family:inherit;font-size:15px;outline:none;transition:border-color .2s,box-shadow .2s;}
.field input::placeholder{color:var(--muted-3);}
.field input:focus{border-color:var(--red);box-shadow:0 0 0 3px var(--red-glow);}
.field input:focus ~ .ficon{color:var(--red-bright);}
.field .eye{position:absolute;right:16px;top:50%;transform:translateY(-50%);color:var(--muted-3);cursor:pointer;font-size:15px;z-index:3;padding:6px;}
.field .eye:hover{color:var(--red-bright);}
.unlock-btn{width:100%;padding:16px;margin-top:8px;border:none;border-radius:12px;cursor:pointer;font-weight:900;font-size:13px;letter-spacing:3px;color:#fff;background:var(--red-gradient);box-shadow:0 8px 30px var(--red-glow);transition:transform .15s,background .3s,box-shadow .3s;display:flex;align-items:center;justify-content:center;gap:12px;font-family:inherit;}
.unlock-btn:hover{transform:translateY(-2px);}
.unlock-btn i{font-size:14px;}
.error-msg{color:#ff6b6b;background:rgba(225,29,46,.1);padding:11px 14px;border-radius:10px;margin-bottom:16px;border:1px solid rgba(225,29,46,.35);font-weight:600;font-size:13px;text-align:center;display:flex;align-items:center;justify-content:center;gap:8px;line-height:1.4;}
.foot-note{text-align:center;margin-top:22px;color:var(--muted-3);font-size:11px;font-weight:600;letter-spacing:.5px;}
.foot-note a{color:var(--red-bright);text-decoration:none;font-weight:800;transition:color .3s;}
</style></head><body>

<div class="login-card">
    <div class="head">
        <div class="login-logo"><img src="{{ banner_image }}" alt="Logo"></div>
        <div class="login-title">HINDUSTAN <span class="r">OSINT</span></div>
        <div class="login-sub">Sign in to access the platform</div>
    </div>
    
    {% if error %}<div class="error-msg"><i class="fas fa-triangle-exclamation"></i> {{ error }}</div>{% endif %}
    <form method="POST" action="/dashboard" autocomplete="off">
        <div class="field">
            <input type="text" name="username" placeholder="Username (optional for master)" autocomplete="off">
            <i class="fas fa-user ficon"></i>
        </div>
        <div class="field">
            <input type="password" name="password" id="pubPass" placeholder="Password" required autocomplete="current-password">
            <i class="fas fa-lock ficon"></i>
            <i class="fas fa-eye eye" onclick="toggleEye()"></i>
        </div>
        <button type="submit" class="unlock-btn"><i class="fas fa-right-to-bracket"></i> SIGN IN</button>
    </form>
    
    <div class="foot-note">Need access? Contact <a href="{{ tg_link }}" target="_blank">Admin</a></div>
</div>

<script>
function toggleEye(){
    var p = document.getElementById('pubPass');
    var e = document.querySelector('.eye');
    if(p.type === 'password'){ p.type = 'text'; e.classList.remove('fa-eye'); e.classList.add('fa-eye-slash'); }
    else { p.type = 'password'; e.classList.remove('fa-eye-slash'); e.classList.add('fa-eye'); }
}
</script>
""" + THEME_SCRIPT + """
</body></html>"""

# ============================================================
# PUBLIC UI TEMPLATE
# ============================================================
PUBLIC_TEMPLATE = """<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Hindustan OSINT</title>
""" + THEME_HEAD + """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
""" + THEME_VARS_CSS + """
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
html{scroll-behavior:smooth;scroll-padding-top:70px;}
html,body{overflow-x:hidden;}
body{background:var(--bg);color:var(--text);font-family:'Inter',sans-serif;min-height:100vh;transition:background .25s,color .25s;}
body::after{content:'';position:fixed;inset:0;z-index:-1;pointer-events:none;background-image:radial-gradient(rgba(255,255,255,.03) 1px,transparent 1px);background-size:26px 26px;}
html.light body::after{background-image:radial-gradient(rgba(0,0,0,.03) 1px,transparent 1px);}
.layout{display:flex;min-height:100vh;}
.sidebar{width:260px;background:var(--card3);backdrop-filter:blur(24px) saturate(150%);border-right:1px solid var(--glass-border);position:fixed;left:0;top:0;height:100vh;height:100dvh;z-index:60;display:flex;flex-direction:column;transition:transform .3s ease,background .25s;overflow:hidden;}
.sb-header{padding:14px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:11px;flex-shrink:0;}
.sb-logo{width:38px;height:38px;border-radius:10px;overflow:hidden;flex-shrink:0;border:1px solid var(--glass-border);}
.sb-logo img{width:100%;height:100%;object-fit:cover;display:block;}
.sb-title{font-weight:800;font-size:13px;color:var(--text);line-height:1.15;letter-spacing:.3px;}
.sb-title .r{color:var(--red-bright);}
.sb-sub{font-size:9.5px;color:var(--muted-2);font-weight:600;letter-spacing:.4px;margin-top:1px;}
.sb-scroll{flex:1;overflow-y:auto;overflow-x:hidden;padding:8px 6px 14px;-webkit-overflow-scrolling:touch;}
.sb-scroll::-webkit-scrollbar{width:5px;}
.sb-scroll::-webkit-scrollbar-thumb{background:var(--red-glow);border-radius:3px;}
.sb-cat{font-size:9.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--muted-3);padding:12px 12px 5px;display:flex;align-items:center;gap:7px;}
.sb-cat i{color:var(--red-bright);font-size:11px;}
.sb-item{display:flex;align-items:center;gap:9px;padding:9px 11px;margin:1px 4px;border-radius:9px;font-size:12.5px;font-weight:600;color:var(--muted);cursor:pointer;transition:all .16s;text-decoration:none;border:1px solid transparent;background:rgba(255,255,255,.02);}
.sb-item:hover{background:rgba(var(--red-r),var(--red-g),var(--red-b),.08);color:var(--text);border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.18);}
.sb-item i{width:17px;text-align:center;font-size:12px;color:var(--red-bright);flex-shrink:0;}
.sb-item .sb-name{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.sb-foot{padding:10px 12px;border-top:1px solid var(--border);font-size:10px;color:var(--muted-3);text-align:center;font-weight:600;letter-spacing:.4px;flex-shrink:0;}
.main{flex:1;margin-left:260px;min-width:0;display:flex;flex-direction:column;}
.top-header{position:sticky;top:0;z-index:40;background:var(--card);backdrop-filter:blur(20px) saturate(150%);border-bottom:1px solid var(--glass-border);height:56px;}
.top-header-inner{max-width:1100px;margin:0 auto;padding:0 16px;display:flex;align-items:center;justify-content:space-between;gap:12px;height:56px;}
.brand-row{display:flex;align-items:center;gap:10px;text-decoration:none;}
.brand-logo{width:32px;height:32px;border-radius:9px;overflow:hidden;flex-shrink:0;border:1px solid var(--glass-border);}
.brand-logo img{width:100%;height:100%;object-fit:cover;display:block;}
.brand-name{font-weight:800;font-size:14.5px;letter-spacing:.4px;color:var(--text);}
.brand-name .r{color:var(--red-bright);}
.hamburger{display:none;background:var(--input-bg-2);border:1px solid var(--glass-border);color:var(--text);font-size:15px;cursor:pointer;padding:0;width:36px;height:36px;border-radius:9px;transition:.2s;align-items:center;justify-content:center;}
.hamburger:hover{color:var(--red-bright);border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.5);}
.header-actions{display:flex;align-items:center;gap:8px;}
.theme-round{height:34px;padding:0 12px;border-radius:9px;background:var(--input-bg-2);border:1px solid var(--glass-border);color:var(--muted);cursor:pointer;font-size:11px;font-weight:800;letter-spacing:1.2px;display:inline-flex;align-items:center;justify-content:center;gap:6px;transition:.2s;font-family:'Inter',sans-serif;text-transform:uppercase;text-decoration:none;}
.theme-round:hover{color:var(--red-bright);border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.5);}
.sb-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.65);backdrop-filter:blur(4px);z-index:55;opacity:0;transition:opacity .3s;}
.sb-overlay.show{display:block;opacity:1;}
.content{max-width:1100px;margin:0 auto;padding:18px 16px 60px;width:100%;min-width:0;}
.cat-block{margin-bottom:22px;min-width:0;}
.cat-label{font-size:10px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--muted-2);padding:6px 2px 10px;display:flex;align-items:center;gap:8px;}
.cat-label i{color:var(--red-bright);font-size:12px;}
.cat-label::after{content:'';flex:1;height:1px;background:var(--border);}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px;min-width:0;}
.ep-card{background:var(--card);backdrop-filter:blur(20px) saturate(140%);border:1px solid var(--glass-border);border-radius:16px;padding:16px;transition:border-color .25s, box-shadow .25s, transform .25s;position:relative;overflow:hidden;cursor:pointer;box-shadow:0 8px 32px rgba(0,0,0,.1), inset 0 1px 0 rgba(255,255,255,.05);scroll-margin-top:72px;min-width:0;}
html.light .ep-card{box-shadow:0 8px 32px rgba(0,0,0,.08), inset 0 1px 0 rgba(255,255,255,.6);}
.ep-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--red),transparent);opacity:0;transition:opacity .25s;}
.ep-card:hover{border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.4);transform:translateY(-2px);box-shadow:0 12px 40px var(--red-glow), inset 0 1px 0 rgba(255,255,255,.06);}
.ep-card:hover::before{opacity:.85;}
.ep-head{display:flex;align-items:center;gap:12px;margin-bottom:12px;min-width:0;}
.ep-head>div{min-width:0;}
.ep-icon{width:44px;height:44px;border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;color:#fff;background:var(--red-gradient);box-shadow:0 6px 20px var(--red-glow);}
.ep-icon.c1{background:linear-gradient(135deg,#6366f1,#8b5cf6);}
.ep-icon.c2{background:linear-gradient(135deg,#f59e0b,#f97316);}
.ep-icon.c3{background:linear-gradient(135deg,#10b981,#06b6d4);}
.ep-icon.c4{background:linear-gradient(135deg,#0ea5e9,#2563eb);}
.ep-icon.c5{background:linear-gradient(135deg,#ec4899,#f43f5e);}
.ep-name{font-weight:800;font-size:14px;color:var(--text);line-height:1.2;word-break:break-word;}
.ep-route{font-family:ui-monospace,Menlo,monospace;font-size:11px;color:var(--red-bright);margin-top:3px;word-break:break-all;opacity:.9;}
.ep-url{background:var(--input-bg);border:1px solid var(--glass-border);border-radius:9px;padding:5px 5px 5px 12px;font-family:ui-monospace,Menlo,monospace;font-size:10.5px;color:var(--muted);line-height:1.5;display:flex;align-items:center;justify-content:space-between;gap:10px;min-height:38px;max-width:100%;}
.ep-url span{min-width:0;flex:1;word-break:break-all;overflow-wrap:anywhere;padding:4px 0;}
.ep-copy{background:var(--red-glow);border:1px solid rgba(var(--red-r),var(--red-g),var(--red-b),.3);color:var(--red-bright);border-radius:7px;font-size:10px;font-weight:800;padding:7px 10px;cursor:pointer;transition:.2s;display:inline-flex;align-items:center;gap:5px;font-family:'Inter',sans-serif;letter-spacing:.5px;flex-shrink:0;white-space:nowrap;}
.ep-copy:hover{background:rgba(var(--red-r),var(--red-g),var(--red-b),.22);}
.ep-copy i{font-size:10px;}
.footer{text-align:center;padding:22px 16px 32px;color:var(--muted-3);font-size:11px;letter-spacing:2px;font-weight:600;}
.footer span{color:var(--red-bright);}
#toast{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(80px);background:var(--red-gradient);color:#fff;padding:11px 18px;border-radius:11px;font-weight:800;font-size:13px;z-index:1000;opacity:0;transition:transform .3s cubic-bezier(.16,1,.3,1),opacity .3s;box-shadow:0 12px 40px var(--red-glow);display:inline-flex;align-items:center;gap:8px;font-family:'Inter',sans-serif;}
#toast.show{transform:translateX(-50%) translateY(0);opacity:1;}
@media(max-width:520px){.grid{grid-template-columns:1fr 1fr;gap:10px;}.ep-card{padding:12px;border-radius:13px;}.ep-icon{width:38px;height:38px;font-size:15px;}.ep-name{font-size:12.5px;}.ep-route{font-size:10px;}.ep-url{font-size:10px;padding:4px 4px 4px 10px;}}
@media(max-width:380px){.grid{grid-template-columns:1fr;}}
@media(max-width:1024px){
    .sidebar{background:var(--card3);box-shadow:8px 0 40px rgba(0,0,0,.65);height:100vh;height:100dvh;transform:translateX(-100%);}
    html.light .sidebar{background:#ffffff;box-shadow:8px 0 40px rgba(0,0,0,.15);}
    .sidebar.open{transform:translateX(0);}
    .main{margin-left:0;}
    .hamburger{display:inline-flex;}
}
</style></head><body>

<div class="sb-overlay" id="sbOverlay" onclick="closeSidebar()"></div>

<div class="layout">
    <aside class="sidebar" id="sidebar">
        <div class="sb-header">
            <div class="sb-logo"><img src="{{ banner_image }}" alt="Logo"></div>
            <div>
                <div class="sb-title">HINDUSTAN <span class="r">OSINT</span></div>
                <div class="sb-sub">Investigation Platform</div>
            </div>
        </div>
        <div class="sb-scroll">
            {% for cat_name, cat_icon, cat_eps in cats %}
                {% set cat_items = [] %}
                {% for ep in cat_eps %}{% if ep in endpoints %}{% set _ = cat_items.append(ep) %}{% endif %}{% endfor %}
                {% if cat_items %}
                <div class="sb-cat"><i class="{{ cat_icon|icls }}"></i> {{ cat_name }}</div>
                {% for ep in cat_items %}
                {% set d = endpoints[ep] %}
                <a class="sb-item" href="#ep-{{ ep }}" onclick="scrollToEp(event,'{{ ep }}')">
                    <i class="{{ d.get('icon','fa-plug')|icls }}"></i>
                    <span class="sb-name">{{ d.get('display_name', ep) }}</span>
                </a>
                {% endfor %}
                {% endif %}
            {% endfor %}

            {% if extra %}
            <div class="sb-cat"><i class="fas fa-cubes"></i> Added by Admin</div>
            {% for ep, d in extra.items() %}
            <a class="sb-item" href="#ep-{{ ep }}" onclick="scrollToEp(event,'{{ ep }}')">
                <i class="{{ d.get('icon','fa-plug')|icls }}"></i>
                <span class="sb-name">{{ d.get('display_name', ep) }}</span>
            </a>
            {% endfor %}
            {% endif %}
        </div>
        
        <div class="side-foot">
            <div class="sb-theme-sec">
                <div class="sb-theme-title">THEME COLORS</div>
                <div class="sb-theme-dots">
                    <div class="theme-dot" data-color="red" onclick="setThemeColor('red')"></div>
                    <div class="theme-dot" data-color="blue" onclick="setThemeColor('blue')"></div>
                    <div class="theme-dot" data-color="green" onclick="setThemeColor('green')"></div>
                    <div class="theme-dot" data-color="orange" onclick="setThemeColor('orange')"></div>
                    <div class="theme-dot" data-color="purple" onclick="setThemeColor('purple')"></div>
                </div>
            </div>
        </div>
        <div class="sb-foot">{{ endpoints|length }} tools</div>
    </aside>

    <main class="main">
        <header class="top-header">
            <div class="top-header-inner">
                <div style="display:flex;align-items:center;gap:10px;">
                    <button class="hamburger" onclick="openSidebar()"><i class="fas fa-bars"></i></button>
                    <a href="/" class="brand-row">
                        <div class="brand-logo"><img src="{{ banner_image }}" alt="Logo"></div>
                        <div class="brand-name">HINDUSTAN <span class="r">OSINT</span></div>
                    </a>
                </div>
                <div class="header-actions">
                    <button class="theme-round" onclick="toggleTheme()"><i class="fas fa-sun theme-icon"></i></button>
                    <a href="/pub/logout" class="theme-round"><i class="fas fa-power-off"></i> LOGOUT</a>
                </div>
            </div>
        </header>

        <div class="content">
            {% for cat_name, cat_icon, cat_eps in cats %}
                {% set cat_items = [] %}
                {% for ep in cat_eps %}{% if ep in endpoints %}{% set _ = cat_items.append(ep) %}{% endif %}{% endfor %}
                {% if cat_items %}
                <div class="cat-block">
                    <div class="cat-label"><i class="{{ cat_icon|icls }}"></i> {{ cat_name }}</div>
                    <div class="grid">
                        {% for ep in cat_items %}
                        {% set d = endpoints[ep] %}{% set cidx = loop.index0 % 6 %}
                        <div class="ep-card" id="ep-{{ ep }}">
                            <div class="ep-head">
                                <div class="ep-icon c{{ cidx }}"><i class="{{ d.get('icon','fa-plug')|icls }}"></i></div>
                                <div style="min-width:0;flex:1">
                                    <div class="ep-name">{{ d.get('display_name', 'Custom API') }}</div>
                                    <div class="ep-route">/api/{{ ep }}</div>
                                </div>
                            </div>
                            <div class="ep-url">
                                <span id="urltext-{{ ep }}">{{ host_url }}api/{{ ep }}?key=YOUR_KEY&{{ d.get('param','query') }}=VALUE</span>
                                <button class="ep-copy" onclick="event.stopPropagation();copyEndpoint('{{ ep }}')"><i class="fas fa-copy"></i> COPY</button>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
                {% endif %}
            {% endfor %}

            {% if extra %}
            <div class="cat-block">
                <div class="cat-label"><i class="fas fa-cubes"></i> Added by Admin</div>
                <div class="grid">
                    {% for ep, d in extra.items() %}
                    {% set cidx = loop.index0 % 6 %}
                    <div class="ep-card" id="ep-{{ ep }}">
                        <div class="ep-head">
                            <div class="ep-icon c{{ cidx }}"><i class="{{ d.get('icon','fa-plug')|icls }}"></i></div>
                            <div style="min-width:0;flex:1">
                                <div class="ep-name">{{ d.get('display_name', ep) }}</div>
                                <div class="ep-route">/api/{{ ep }}</div>
                            </div>
                        </div>
                        <div class="ep-url">
                            <span id="urltext-{{ ep }}">{{ host_url }}api/{{ ep }}?key=YOUR_KEY&{{ d.get('param','query') }}=VALUE</span>
                            <button class="ep-copy" onclick="event.stopPropagation();copyEndpoint('{{ ep }}')"><i class="fas fa-copy"></i> COPY</button>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}

            <div class="footer">HINDUSTAN OSINT <span>·</span> CYBER SECURITY <span>·</span></div>
        </div>
    </main>
</div>

<div id="toast"><i class="fas fa-check-circle"></i> <span id="toastMsg">COPIED</span></div>

<script>
function openSidebar(){document.getElementById('sidebar').classList.add('open');document.getElementById('sbOverlay').classList.add('show');document.body.style.overflow='hidden';}
function closeSidebar(){document.getElementById('sidebar').classList.remove('open');document.getElementById('sbOverlay').classList.remove('show');document.body.style.overflow='';}
window.addEventListener('resize', function(){ if(window.innerWidth > 1024) closeSidebar(); });
function scrollToEp(e, ep){
    if(e) e.preventDefault(); closeSidebar();
    var el = document.getElementById('ep-' + ep); if(!el) return;
    var header = document.querySelector('.top-header');
    var headerH = header ? header.getBoundingClientRect().height : 0;
    var top = el.getBoundingClientRect().top + window.pageYOffset - headerH - 12;
    if(top < 0) top = 0;
    window.scrollTo({top: top, behavior: 'smooth'});
}
function copyEndpoint(ep){
    var el = document.getElementById('urltext-' + ep); if(!el) return;
    var text = el.textContent.trim();
    function done(){var t=document.getElementById('toast');document.getElementById('toastMsg').textContent='COPIED';t.classList.add('show');clearTimeout(window.__toastT);window.__toastT=setTimeout(function(){t.classList.remove('show');},1600);}
    function fallback(){var ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();try{document.execCommand('copy');done();}catch(e){}ta.remove();}
    if(navigator.clipboard && navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(done).catch(fallback);} else { fallback(); }
}
</script>
""" + THEME_SCRIPT + """
</body></html>"""

# ============================================================
# RESELLER LOGIN TEMPLATE
# ============================================================
RESELLER_LOGIN_TEMPLATE = """<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, viewport-fit=cover">
<title>Reseller — Hindustan OSINT</title>
""" + THEME_HEAD + """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
""" + THEME_VARS_CSS + """
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent;}
html,body{overflow-x:hidden;}
body{background:var(--bg);color:var(--text);font-family:'Inter',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;transition:background .25s,color .25s;}
.login-card{position:relative;z-index:2;width:100%;max-width:430px;padding:46px 28px 30px;border-radius:22px;background:var(--card);backdrop-filter:blur(26px) saturate(150%);border:1px solid var(--glass-border);box-shadow:0 20px 60px rgba(0,0,0,.2), inset 0 1px 0 rgba(255,255,255,.08), 0 0 80px var(--red-glow);animation:cardIn .55s cubic-bezier(.22,.9,.35,1.2) both;transition:box-shadow .3s;}
html.light .login-card{box-shadow:0 20px 60px rgba(0,0,0,.08), inset 0 1px 0 rgba(255,255,255,.7), 0 0 60px var(--red-glow);}
@keyframes cardIn{from{opacity:0;transform:translateY(24px) scale(.95);}to{opacity:1;transform:none;}}
.head{display:flex;flex-direction:column;align-items:center;margin-bottom:4px;}
.login-logo{width:80px;height:80px;border-radius:20px;overflow:hidden;border:1px solid var(--glass-border);box-shadow:0 12px 40px var(--red-glow);margin-bottom:14px;}
.login-logo img{width:100%;height:100%;object-fit:cover;display:block;}
.login-title{text-align:center;font-size:22px;font-weight:900;letter-spacing:1.2px;margin-bottom:4px;}
.login-title .r{color:var(--red-bright);}
.login-sub{text-align:center;color:var(--muted-2);font-size:12.5px;font-weight:500;margin-bottom:26px;}
.field{position:relative;margin-bottom:14px;}
.field .ficon{position:absolute;left:18px;top:50%;transform:translateY(-50%);color:var(--muted-3);font-size:15px;pointer-events:none;z-index:2;}
.field input{width:100%;padding:17px 48px 17px 48px;background:var(--input-bg-2);border:1px solid var(--glass-border);border-radius:12px;color:var(--text);font-family:inherit;font-size:15px;outline:none;transition:border-color .2s,box-shadow .2s;}
.field input::placeholder{color:var(--muted-3);}
.field input:focus{border-color:var(--red);box-shadow:0 0 0 3px var(--red-glow);}
.field .eye{position:absolute;right:16px;top:50%;transform:translateY(-50%);color:var(--muted-3);cursor:pointer;font-size:15px;z-index:3;padding:6px;}
.unlock-btn{width:100%;padding:16px;margin-top:8px;border:none;border-radius:12px;cursor:pointer;font-weight:900;font-size:13px;letter-spacing:3px;color:#fff;background:var(--red-gradient);box-shadow:0 8px 30px var(--red-glow);transition:transform .15s;display:flex;align-items:center;justify-content:center;gap:12px;font-family:inherit;}
.unlock-btn:hover{transform:translateY(-2px);}
.unlock-btn i{font-size:14px;}
.error-msg{color:#ff6b6b;background:rgba(225,29,46,.1);padding:11px 14px;border-radius:10px;margin-bottom:16px;border:1px solid rgba(225,29,46,.35);font-weight:600;font-size:13px;text-align:center;display:flex;align-items:center;justify-content:center;gap:8px;line-height:1.4;}
.foot-note{text-align:center;margin-top:22px;color:var(--muted-3);font-size:11px;font-weight:600;}
.foot-note a{color:var(--red-bright);text-decoration:none;font-weight:800;}
</style></head><body>
<div class="login-card">
    <div class="head">
        <div class="login-logo"><img src="{{ banner_image }}" alt="Logo"></div>
        <div class="login-title">HINDUSTAN <span class="r">RESELLER</span></div>
        <div class="login-sub">Reseller Login</div>
    </div>
    
    {% if error %}<div class="error-msg"><i class="fas fa-triangle-exclamation"></i> {{ error }}</div>{% endif %}
    <form method="POST" action="/reseller" autocomplete="off">
        <div class="field">
            <input type="text" name="username" placeholder="Reseller Username" required autocomplete="off" autofocus>
            <i class="fas fa-user ficon"></i>
        </div>
        <div class="field">
            <input type="password" name="password" id="rslrPass" placeholder="Reseller Password" required autocomplete="current-password">
            <i class="fas fa-lock ficon"></i>
            <i class="fas fa-eye eye" onclick="toggleEye()"></i>
        </div>
        <button type="submit" class="unlock-btn"><i class="fas fa-right-to-bracket"></i> SIGN IN</button>
    </form>
    
    <div class="foot-note">Need an account? Contact <a href="{{ tg_link }}" target="_blank">Admin</a></div>
</div>
<script>
function toggleEye(){
    var p = document.getElementById('rslrPass');
    var e = document.querySelector('.eye');
    if(p.type === 'password'){ p.type = 'text'; e.classList.remove('fa-eye'); e.classList.add('fa-eye-slash'); }
    else { p.type = 'password'; e.classList.remove('fa-eye-slash'); e.classList.add('fa-eye'); }
}
</script>
""" + THEME_SCRIPT + """
</body></html>"""

RESELLER_EXPIRED_TEMPLATE = """<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Plan Expired — Hindustan OSINT</title>
""" + THEME_HEAD + """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
""" + THEME_VARS_CSS + """
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:'Inter',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;}
.card{max-width:460px;width:100%;padding:40px 28px;border-radius:24px;background:var(--card);backdrop-filter:blur(26px) saturate(150%);border:1px solid var(--glass-border);box-shadow:0 20px 60px rgba(0,0,0,.5),0 0 80px var(--red-glow);text-align:center;}
.icon-wrap{width:96px;height:96px;margin:0 auto 24px;border-radius:24px;background:var(--red-gradient);display:flex;align-items:center;justify-content:center;color:#fff;font-size:42px;box-shadow:0 14px 44px var(--red-glow);}
h1{font-size:24px;font-weight:900;letter-spacing:1.2px;margin-bottom:12px;}
h1 .r{color:var(--red-bright);}
p{color:var(--muted);font-size:14.5px;line-height:1.65;margin-bottom:26px;}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;padding:15px 26px;border-radius:12px;background:var(--red-gradient);color:#fff;text-decoration:none;font-weight:800;font-size:13px;letter-spacing:1.5px;box-shadow:0 8px 30px var(--red-glow);transition:.2s;}
.btn:hover{transform:translateY(-2px);}
.note{color:var(--muted-3);font-size:11px;letter-spacing:1.5px;margin-top:20px;font-weight:700;text-transform:uppercase;}
</style></head><body>
<div class="card">
    <div class="icon-wrap"><i class="fas fa-hourglass-end"></i></div>
    <h1>PLAN <span class="r">EXPIRED</span></h1>
    <p>Your reseller plan has ended. To continue using the platform, please contact the admin to renew your subscription.</p>
    <a class="btn" href="{{ tg_link }}" target="_blank"><i class="fab fa-telegram"></i> CONTACT ADMIN</a>
    <div class="note">Hindustan OSINT · Reseller</div>
</div>
</body></html>"""

RESELLER_PANEL_TEMPLATE = """<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, viewport-fit=cover">
<title>Reseller Dashboard — Hindustan OSINT</title>
""" + THEME_HEAD + """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&display=swap');
""" + THEME_VARS_CSS + """
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent;}
html{scroll-behavior:smooth;}
html,body{overflow-x:hidden;}
body{background:var(--bg);color:var(--text);font-family:'Rajdhani',sans-serif;padding-bottom:80px;transition:background .25s,color .25s;}
body::after{content:'';position:fixed;inset:0;z-index:-1;pointer-events:none;background-image:radial-gradient(rgba(255,255,255,.03) 1px,transparent 1px);background-size:26px 26px;}
html.light body::after{background-image:radial-gradient(rgba(0,0,0,.03) 1px,transparent 1px);}
h1,h2,h3,.brand-name,.pill-btn{font-family:'Orbitron',sans-serif;}

.shell{display:flex;min-height:100vh;}
.sidebar{width:240px;background:var(--card3);backdrop-filter:blur(24px) saturate(150%);border-right:1px solid var(--glass-border);padding:18px 12px;position:fixed;top:0;left:0;height:100vh;height:100dvh;overflow-y:auto;z-index:60;display:flex;flex-direction:column;transition:transform .3s ease,background .25s;}
.brand{display:flex;align-items:center;gap:11px;padding:0 8px 16px;border-bottom:1px solid var(--border);margin-bottom:12px;}
.brand-logo{width:38px;height:38px;border-radius:10px;overflow:hidden;flex-shrink:0;border:1px solid var(--glass-border);}
.brand-logo img{width:100%;height:100%;object-fit:cover;display:block;}
.brand-text{display:flex;flex-direction:column;line-height:1.1;min-width:0;}
.brand-name{font-weight:700;letter-spacing:1.2px;font-size:12px;}
.brand-name .r{color:var(--red-bright);}
.brand-sub{color:var(--muted-3);font-size:9px;letter-spacing:1.5px;font-weight:600;margin-top:1px;}
.nav-label{color:var(--muted-3);font-size:10px;letter-spacing:2px;padding:12px 10px 6px;font-weight:700;}
.nav-item{display:flex;align-items:center;gap:12px;padding:11px 14px;border-radius:10px;color:var(--muted);text-decoration:none;font-weight:600;font-size:13.5px;cursor:pointer;transition:.2s;border:1px solid transparent;background:transparent;width:100%;text-align:left;font-family:inherit;}
.nav-item:hover{background:rgba(var(--red-r),var(--red-g),var(--red-b),.08);color:var(--text);border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.18);}
.nav-item.active{background:linear-gradient(90deg,var(--red-glow),transparent);color:var(--red-bright);border-left:3px solid var(--red);padding-left:11px;}
.nav-item i{width:18px;text-align:center;font-size:14px;}
.nav-count{margin-left:auto;background:var(--red-glow);color:var(--red-bright);font-size:10px;font-weight:800;padding:2px 8px;border-radius:99px;border:1px solid rgba(var(--red-r),var(--red-g),var(--red-b),.35);}
.side-foot{margin-top:auto;}
.main{flex:1;margin-left:240px;padding:22px 24px 100px;min-width:0;}
.topbar-m{display:flex;align-items:center;justify-content:space-between;margin-bottom:22px;gap:12px;flex-wrap:wrap;}
.greet h1{font-size:22px;font-weight:700;} .greet p{color:var(--muted-2);font-size:12px;margin-top:3px;}
.top-actions{display:flex;gap:10px;align-items:center;flex-wrap:wrap;}
.icon-btn{width:38px;height:38px;border-radius:10px;background:var(--input-bg-2);border:1px solid var(--glass-border);color:var(--muted);cursor:pointer;font-size:14px;display:flex;align-items:center;justify-content:center;text-decoration:none;transition:.2s;}
.icon-btn:hover{color:var(--red-bright);border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.5);}
.theme-round{height:38px;padding:0 14px;border-radius:10px;background:var(--input-bg-2);border:1px solid var(--glass-border);color:var(--muted);cursor:pointer;font-size:11px;font-family:'Orbitron',sans-serif;font-weight:700;letter-spacing:1.5px;display:inline-flex;align-items:center;justify-content:center;gap:7px;transition:.2s;text-transform:uppercase;}
.theme-round:hover{color:var(--red-bright);border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.5);}
.pill-btn{padding:9px 16px;border-radius:10px;background:var(--red-gradient);color:#fff;border:none;font-weight:700;font-family:inherit;font-size:13px;cursor:pointer;letter-spacing:.5px;display:inline-flex;align-items:center;gap:8px;justify-content:center;box-shadow:0 4px 14px rgba(var(--red-r),var(--red-g),var(--red-b),.35);transition:transform .15s;}
.pill-btn:hover{transform:translateY(-1px);}
.pill-btn i{font-size:12px;}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:24px;}
.stat{background:var(--card);backdrop-filter:blur(20px) saturate(140%);border:1px solid var(--glass-border);border-radius:14px;padding:18px;position:relative;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,.1), inset 0 1px 0 rgba(255,255,255,.05);}
.stat::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--red),transparent);opacity:.7;}
.stat.green::after{background:linear-gradient(90deg,transparent,var(--green),transparent);}
.stat.purple::after{background:linear-gradient(90deg,transparent,var(--purple),transparent);}
.stat .label{color:var(--muted-2);font-size:10px;letter-spacing:2px;font-weight:700;}
.stat .value{font-family:'Orbitron';font-size:28px;font-weight:700;margin-top:8px;line-height:1;}
.stat .value.green{color:var(--green);}
.stat .value.red{color:var(--red-bright);}
.stat .value.warn{color:var(--maint);}
.stat .value.purple{color:var(--purple);}
.stat .delta{color:var(--muted-2);font-size:11px;margin-top:8px;font-weight:600;}
.stat .corner{position:absolute;top:16px;right:16px;font-size:18px;color:var(--red);opacity:.85;}
.stat.green .corner{color:var(--green);}
.stat.purple .corner{color:var(--purple);}
.card{background:var(--card);backdrop-filter:blur(20px) saturate(140%);border:1px solid var(--glass-border);border-radius:16px;padding:20px;margin-bottom:22px;box-shadow:0 8px 32px rgba(0,0,0,.1), inset 0 1px 0 rgba(255,255,255,.05);}
.card-title{display:flex;align-items:center;gap:10px;font-size:15px;font-weight:700;margin-bottom:18px;}
.card-title i{color:var(--red-bright);font-size:15px;}
.card-title .hint{color:var(--muted-3);font-size:11px;margin-left:auto;letter-spacing:1px;font-weight:600;}
.form-label{color:var(--muted);font-size:11px;letter-spacing:2px;font-weight:700;margin:14px 0 8px;display:block;}
.form-control{width:100%;padding:12px 14px;background:var(--input-bg);border:1px solid var(--glass-border);color:var(--text);border-radius:10px;outline:none;font-family:inherit;font-size:14px;transition:.2s;}
.form-control::placeholder{color:var(--muted-3);}
.form-control:focus{border-color:var(--red);box-shadow:0 0 0 3px var(--red-glow);}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
@media(max-width:600px){.grid-2{grid-template-columns:1fr;}}
.rslr-picker{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;max-height:280px;overflow-y:auto;padding:10px;background:var(--input-bg);border:1px solid var(--glass-border);border-radius:12px;margin-top:6px;}
.rslr-picker::-webkit-scrollbar{width:6px;}
.rslr-picker::-webkit-scrollbar-thumb{background:var(--red-glow);border-radius:3px;}
.rslr-item{display:flex;align-items:center;gap:8px;padding:9px 10px;border-radius:9px;background:var(--input-bg-2);border:1.5px solid var(--glass-border);cursor:pointer;transition:.15s;user-select:none;font-size:12px;font-weight:600;}
.rslr-item:hover{border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.4);}
.rslr-item.on{border-color:var(--red);background:var(--red-glow);}
.rslr-item i{font-size:12px;color:var(--muted-2);flex-shrink:0;}
.rslr-item.on i{color:var(--red-bright);}
.rslr-item span{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--muted);}
.rslr-item.on span{color:var(--red-bright);}
.rslr-item input{display:none;}
.rslr-toolbar{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap;align-items:center;}
.rslr-toolbar button{padding:7px 12px;border-radius:8px;background:var(--input-bg-2);border:1px solid var(--glass-border);color:var(--muted);font-family:inherit;font-size:11.5px;font-weight:700;cursor:pointer;transition:.2s;}
.rslr-toolbar button:hover{color:var(--red-bright);border-color:rgba(var(--red-r),var(--red-g),var(--red-b),.4);}
.rslr-toolbar .count{margin-left:auto;font-size:11px;color:var(--muted-2);font-weight:700;}
.apikey-row{background:var(--input-bg-2);padding:16px;border-radius:14px;border-left:3px solid var(--red);margin-bottom:12px;}
.apikey-row.expired{border-left-color:var(--muted-3);opacity:.75;}
.apikey-head{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:12px;}
.apikey-ico{width:42px;height:42px;border-radius:11px;background:var(--red-glow);border:1px solid rgba(var(--red-r),var(--red-g),var(--red-b),.25);color:var(--red-bright);display:flex;align-items:center;justify-content:center;font-size:17px;flex-shrink:0;}
.apikey-row.expired .apikey-ico{background:rgba(120,120,120,.15);border-color:rgba(120,120,120,.3);color:var(--muted);}
.apikey-meta{flex:1;min-width:180px;}
.apikey-name{font-weight:700;font-size:15px;color:var(--text);word-break:break-all;}
.apikey-sub{font-size:11.5px;color:var(--muted-2);margin-top:3px;display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
.apikey-badges{display:flex;gap:6px;flex-wrap:wrap;}
.apikey-url-box{background:var(--input-bg);border:1px solid var(--glass-border);border-radius:9px;padding:11px 12px;display:flex;align-items:center;gap:10px;font-family:ui-monospace,monospace;font-size:11px;color:var(--muted);word-break:break-all;overflow-wrap:anywhere;line-height:1.5;min-width:0;margin-bottom:8px;}
.apikey-url-box code{flex:1;min-width:0;color:var(--red-bright);font-weight:700;word-break:break-all;overflow-wrap:anywhere;}
.apikey-url-box button{background:var(--red-glow);border:1px solid rgba(var(--red-r),var(--red-g),var(--red-b),.3);color:var(--red-bright);border-radius:7px;font-size:10px;font-weight:800;padding:6px 10px;cursor:pointer;font-family:inherit;flex-shrink:0;display:inline-flex;align-items:center;gap:4px;letter-spacing:.4px;text-transform:uppercase;}
.apikey-url-box button:hover{background:rgba(var(--red-r),var(--red-g),var(--red-b),.22);}
.apikey-actions{display:flex;gap:6px;flex-wrap:wrap;}
.del-btn{background:var(--red-glow);border:1px solid rgba(var(--red-r),var(--red-g),var(--red-b),.4);color:var(--red-bright);padding:7px 12px;border-radius:8px;cursor:pointer;font-size:11.5px;font-family:inherit;font-weight:700;display:inline-flex;align-items:center;gap:5px;}
.del-btn:hover{background:rgba(var(--red-r),var(--red-g),var(--red-b),.25);}
.edit-btn{background:rgba(139,92,246,.15);border:1px solid rgba(139,92,246,.4);color:var(--purple);padding:7px 12px;border-radius:8px;cursor:pointer;font-size:11.5px;font-family:inherit;font-weight:700;display:inline-flex;align-items:center;gap:5px;}
.edit-btn:hover{background:rgba(139,92,246,.28);}
.badge{display:inline-block;padding:3px 9px;border-radius:6px;font-size:10px;font-weight:700;letter-spacing:.8px;}
.badge.on{background:var(--green-glow);color:var(--green);border:1px solid rgba(16,185,129,.4);}
.badge.off{background:rgba(120,120,120,.15);color:var(--muted);border:1px solid rgba(120,120,120,.3);}
.section{display:none;} .section.active{display:block;animation:fade .25s;}
@keyframes fade{from{opacity:0;transform:translateY(6px);}to{opacity:1;transform:none;}}
.mob-topbar{display:none;position:sticky;top:0;z-index:45;background:var(--card);backdrop-filter:blur(20px) saturate(150%);border-bottom:1px solid var(--glass-border);padding:11px 14px;align-items:center;justify-content:space-between;gap:10px;}
.mob-topbar .mt-left{display:flex;align-items:center;gap:10px;min-width:0;}
.mob-topbar .mt-logo{width:32px;height:32px;border-radius:9px;overflow:hidden;flex-shrink:0;border:1px solid var(--glass-border);}
.mob-topbar .mt-logo img{width:100%;height:100%;object-fit:cover;display:block;}
.mob-topbar .mt-title{font-family:'Orbitron',sans-serif;font-weight:700;font-size:12px;letter-spacing:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.mob-topbar .mt-title .r{color:var(--red-bright);}
.mob-burger{background:var(--input-bg-2);border:1px solid var(--glass-border);color:var(--text);font-size:15px;width:36px;height:36px;border-radius:9px;display:inline-flex;align-items:center;justify-content:center;cursor:pointer;}
.sb-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.65);backdrop-filter:blur(4px);z-index:55;opacity:0;transition:opacity .3s;}
.sb-overlay.show{display:block;opacity:1;}
.mob-nav{position:fixed;bottom:0;left:0;right:0;background:var(--card3);backdrop-filter:blur(24px) saturate(150%);border-top:1px solid var(--glass-border);display:none;z-index:100;padding:8px 4px calc(8px + env(safe-area-inset-bottom));justify-content:space-around;}
.mob-tab{background:transparent;border:none;color:var(--muted-2);font-family:inherit;font-size:10px;display:flex;flex-direction:column;align-items:center;gap:4px;padding:8px 4px;border-radius:10px;cursor:pointer;flex:1;font-weight:700;}
.mob-tab i{font-size:17px;}
.mob-tab.active{color:var(--red-bright);background:var(--red-glow);}
#toast{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(80px);background:linear-gradient(135deg,#10b981,#059669);color:#fff;padding:12px 20px;border-radius:11px;font-weight:800;font-size:13px;z-index:1000;opacity:0;transition:transform .3s cubic-bezier(.16,1,.3,1),opacity .3s;box-shadow:0 12px 40px rgba(16,185,129,.4);display:inline-flex;align-items:center;gap:8px;font-family:inherit;}
#toast.show{transform:translateX(-50%) translateY(0);opacity:1;}
.modal-bg{display:none;position:fixed;inset:0;background:rgba(0,0,0,.85);backdrop-filter:blur(8px);z-index:200;align-items:center;justify-content:center;padding:20px;overflow-y:auto;}
html.light .modal-bg{background:rgba(0,0,0,.5);}
.modal-bg.open{display:flex;}
.modal{background:var(--card2);backdrop-filter:blur(24px) saturate(150%);border:1px solid var(--glass-border);border-radius:18px;max-width:520px;width:100%;padding:26px 22px;box-shadow:var(--shadow-card),0 0 60px var(--red-glow);margin:auto;max-height:calc(100vh - 40px);overflow-y:auto;}
.modal h3{font-size:16px;color:var(--red-bright);margin-bottom:6px;letter-spacing:1px;display:flex;align-items:center;gap:10px;}
.modal .sub{color:var(--muted-2);font-size:12px;margin-bottom:20px;}
.modal .row{display:flex;gap:10px;margin-top:20px;}
.modal .row button{flex:1;padding:12px;border-radius:10px;font-family:inherit;font-weight:700;font-size:13px;cursor:pointer;border:none;}
.modal .cancel{background:var(--input-bg-2);color:var(--muted);border:1px solid var(--glass-border);}
.modal .save{background:var(--red-gradient);color:#fff;}
@media(max-width:900px){
    .sidebar{background:var(--card3);box-shadow:8px 0 40px rgba(0,0,0,.65);height:100vh;height:100dvh;transform:translateX(-100%);width:250px;}
    html.light .sidebar{background:#ffffff;box-shadow:8px 0 40px rgba(0,0,0,.15);}
    .sidebar.open{transform:translateX(0);}
    body{padding-bottom:88px;}
    .main{margin-left:0;padding:14px 12px 100px;}
    .mob-topbar{display:flex;}
    .mob-nav{display:flex;}
    .stats{grid-template-columns:repeat(2,1fr);gap:10px;}
    .stat{padding:14px;border-radius:13px;}
    .stat .value{font-size:22px;}
    .topbar-m{display:none;}
    .card{padding:16px;border-radius:14px;margin-bottom:16px;}
    .grid-2{grid-template-columns:1fr;gap:10px;}
    .rslr-picker{grid-template-columns:repeat(2,1fr);}
}
@media(max-width:520px){
    .stats{grid-template-columns:1fr 1fr;gap:8px;}
    .stat{padding:12px;border-radius:12px;}
    .stat .value{font-size:19px;}
    .rslr-picker{grid-template-columns:1fr;}
}
</style></head><body>

<div class="sb-overlay" id="sbOverlay" onclick="closeSidebar()"></div>

<div class="shell">
    <aside class="sidebar" id="rslrSidebar">
        <div class="brand">
            <div class="brand-logo"><img src="{{ banner_image }}" alt="Logo"></div>
            <div class="brand-text">
                <span class="brand-name">HINDUSTAN <span class="r">RESELLER</span></span>
                <span class="brand-sub">SELLER PANEL</span>
            </div>
        </div>
        <div class="nav-label">MAIN</div>
        <button class="nav-item active" data-sec="dashboard" onclick="go('dashboard')"><i class="fas fa-table-cells-large"></i> Dashboard</button>
        <button class="nav-item" data-sec="create" onclick="go('create')"><i class="fas fa-plus"></i> Create API Key</button>
        <button class="nav-item" data-sec="mykeys" onclick="go('mykeys')"><i class="fas fa-key"></i> My Keys <span class="nav-count">{{ my_keys|length }}</span></button>
        <button class="nav-item" data-sec="features" onclick="go('features')"><i class="fas fa-cubes"></i> My Features <span class="nav-count">{{ reseller_eps|length }}</span></button>
        <div class="nav-label">LINK</div>
        <a class="nav-item" href="/" target="_blank"><i class="fas fa-globe"></i> Public Site</a>
        <a class="nav-item" href="{{ tg_link }}" target="_blank"><i class="fab fa-telegram"></i> Support</a>
        
        <div class="side-foot">
            <div class="sb-theme-sec">
                <div class="sb-theme-title">THEME COLORS</div>
                <div class="sb-theme-dots">
                    <div class="theme-dot" data-color="red" onclick="setThemeColor('red')"></div>
                    <div class="theme-dot" data-color="blue" onclick="setThemeColor('blue')"></div>
                    <div class="theme-dot" data-color="green" onclick="setThemeColor('green')"></div>
                    <div class="theme-dot" data-color="orange" onclick="setThemeColor('orange')"></div>
                    <div class="theme-dot" data-color="purple" onclick="setThemeColor('purple')"></div>
                </div>
            </div>
            <a class="nav-item" href="/reseller/logout" style="color:#ef4444;margin:8px 10px 0;"><i class="fas fa-power-off"></i> Logout</a>
        </div>
    </aside>

    <main class="main">
        <div class="mob-topbar">
            <div class="mt-left">
                <button class="mob-burger" onclick="openSidebar()"><i class="fas fa-bars"></i></button>
                <div class="mt-logo"><img src="{{ banner_image }}" alt="Logo"></div>
                <div class="mt-title">HINDUSTAN <span class="r">RESELLER</span></div>
            </div>
            <div style="display:flex;gap:8px;align-items:center;">
                <button class="mob-burger" onclick="toggleTheme()"><i class="fas fa-sun theme-icon"></i></button>
                <a href="/reseller/logout" class="mob-burger" style="color:#ef4444;"><i class="fas fa-power-off"></i></a>
            </div>
        </div>

        <div class="topbar-m">
            <div class="greet"><h1 id="greet-title">Welcome back</h1><p>{{ days_left }} days left · {{ expires_display }}</p></div>
            <div class="top-actions">
                <button class="theme-round" onclick="toggleTheme()"><i class="fas fa-sun theme-icon"></i> <span class="theme-text">DAY</span></button>
                <a href="/" target="_blank" class="icon-btn" title="Public site"><i class="fas fa-globe"></i></a>
                <a href="{{ tg_link }}" target="_blank" class="icon-btn" title="Support"><i class="fab fa-telegram"></i></a>
                <a href="/reseller/logout" class="icon-btn" style="color:#ef4444;" title="Logout"><i class="fas fa-power-off"></i></a>
            </div>
        </div>

        <section id="sec-dashboard" class="section active">
            <div class="stats">
                <div class="stat {% if days_left <= 3 %}stat{% else %}green{% endif %}">
                    <div class="corner"><i class="fas fa-hourglass-half"></i></div>
                    <div class="label">DAYS LEFT</div>
                    <div class="value {% if days_left <= 3 %}red{% elif days_left <= 7 %}warn{% else %}green{% endif %}">{{ days_left }}</div>
                    <div class="delta">Expires {{ expires_display }}</div>
                </div>
                <div class="stat"><div class="corner"><i class="fas fa-key"></i></div>
                    <div class="label">MY KEYS</div><div class="value">{{ my_keys|length }}</div>
                    <div class="delta">Generated</div></div>
                <div class="stat purple"><div class="corner"><i class="fas fa-cubes"></i></div>
                    <div class="label">FEATURES</div><div class="value purple">{{ reseller_eps|length }}</div>
                    <div class="delta">Granted by admin</div></div>
                <div class="stat"><div class="corner"><i class="fas fa-chart-line"></i></div>
                    <div class="label">TOTAL CALLS</div><div class="value">{{ calls_used }}</div>
                    <div class="delta">Across all keys</div></div>
            </div>

            <div class="card">
                <div class="card-title"><i class="fas fa-bolt"></i> Quick Start <span class="hint">3 steps</span></div>
                <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;">
                    <div style="background:var(--input-bg-2);padding:14px;border-radius:12px;border-left:3px solid var(--red);">
                        <div style="font-weight:800;font-size:13px;color:var(--red-bright);letter-spacing:1px;margin-bottom:5px;">1. CREATE KEY</div>
                        <div style="font-size:12.5px;color:var(--muted);line-height:1.55;">Name dalo, features select karo, days set karo. Key auto ban jaayegi.</div>
                    </div>
                    <div style="background:var(--input-bg-2);padding:14px;border-radius:12px;border-left:3px solid var(--red);">
                        <div style="font-weight:800;font-size:13px;color:var(--red-bright);letter-spacing:1px;margin-bottom:5px;">2. COPY LINK</div>
                        <div style="font-size:12.5px;color:var(--muted);line-height:1.55;">My Keys tab me har key ka ready URL hai. COPY button se copy karo.</div>
                    </div>
                    <div style="background:var(--input-bg-2);padding:14px;border-radius:12px;border-left:3px solid var(--red);">
                        <div style="font-weight:800;font-size:13px;color:var(--red-bright);letter-spacing:1px;margin-bottom:5px;">3. SELL</div>
                        <div style="font-size:12.5px;color:var(--muted);line-height:1.55;">Wo URL customer ko do. Customer us URL me VALUE ki jagah data daale.</div>
                    </div>
                </div>
            </div>
        </section>

        <section id="sec-create" class="section">
            <div class="card">
                <div class="card-title"><i class="fas fa-plus-circle"></i> Create API Key <span class="hint">auto-generated</span></div>
                {% if days_left <= 0 or reseller_eps|length == 0 %}
                    <p style="text-align:center;color:var(--red-bright);padding:30px;font-weight:700;">
                        {% if days_left <= 0 %}Plan expired.{% else %}No features granted by admin yet.{% endif %}
                    </p>
                {% else %}
                <form method="POST" action="/reseller/create_key">
                    <div class="grid-2">
                        <div>
                            <label class="form-label">KEY NAME</label>
                            <input type="text" name="key_name" class="form-control" placeholder="e.g. vip1, ramesh, sept" required pattern="[a-zA-Z0-9_\\-]+" autocomplete="off">
                        </div>
                        <div>
                            <label class="form-label">DURATION (DAYS) — MAX {{ days_left }}</label>
                            <input type="number" name="key_days" class="form-control" value="{% if days_left >= 30 %}30{% else %}{{ days_left }}{% endif %}" min="1" max="{{ days_left }}" required>
                        </div>
                    </div>
                    <label class="form-label">SELECT FEATURES — {{ reseller_eps|length }} available</label>
                    <input type="text" class="icon-picker-search" id="kSearch" placeholder="Search feature..." style="width:100%;padding:9px 12px;background:var(--input-bg-2);border:1px solid var(--glass-border);border-radius:9px;color:var(--text);font-family:inherit;font-size:13px;outline:none;margin-top:6px;">
                    <div class="rslr-picker" id="kPicker">
                        {% for ep in reseller_eps %}
                        {% set d = endpoints[ep] %}
                        <label class="rslr-item" data-name="{{ ep }} {{ d.get('display_name','') }}">
                            <input type="checkbox" name="key_features" value="{{ ep }}">
                            <i class="{{ d.get('icon','fa-plug')|icls }}"></i>
                            <span>{{ d.get('display_name', ep) }}</span>
                        </label>
                        {% endfor %}
                    </div>
                    <div class="rslr-toolbar">
                        <button type="button" onclick="keySelectAll(true)"><i class="fas fa-check-double"></i> Select All</button>
                        <button type="button" onclick="keySelectAll(false)"><i class="fas fa-xmark"></i> Clear</button>
                        <span class="count"><span id="kCount">0</span> selected</span>
                    </div>
                    <button type="submit" class="pill-btn" style="margin-top:18px;padding:13px 20px;width:100%;">
                        <i class="fas fa-key"></i> Generate Key
                    </button>
                </form>
                {% endif %}
            </div>
        </section>

        <section id="sec-mykeys" class="section">
            <div class="card">
                <div class="card-title"><i class="fas fa-key"></i> My API Keys <span class="hint">{{ my_keys|length }} total</span></div>
                {% if my_keys %}
                    {% for kn, k in my_keys.items() %}
                    <div class="apikey-row {% if not k.is_active %}expired{% endif %}">
                        <div class="apikey-head">
                            <div class="apikey-ico"><i class="fas fa-key"></i></div>
                            <div class="apikey-meta">
                                <div class="apikey-name">{{ kn }}</div>
                                <div class="apikey-sub">
                                    <span><i class="fas fa-calendar"></i> {{ k.days }}d</span>
                                    <span><i class="fas fa-cubes"></i> {{ k.features_count }} features</span>
                                    <span><i class="fas fa-chart-line"></i> {{ k.calls_used }} calls</span>
                                    <span><i class="fas fa-clock"></i> expires {{ k.expires_display }}</span>
                                </div>
                            </div>
                            <div class="apikey-badges">
                                {% if k.is_active %}<span class="badge on">ACTIVE</span>{% else %}<span class="badge off">EXPIRED</span>{% endif %}
                            </div>
                        </div>
                        <div class="apikey-url-box">
                            <code id="key-{{ kn }}">{{ k.api_key }}</code>
                            <button onclick="copyKeyVal('{{ kn }}')"><i class="fas fa-copy"></i> KEY</button>
                        </div>
                        <div class="apikey-url-box">
                            <code id="lnk-{{ kn }}">{{ k.sample_link }}</code>
                            <button onclick="copyLinkVal('{{ kn }}')"><i class="fas fa-link"></i> URL</button>
                        </div>
                        <div class="apikey-actions">
                            <button type="button" class="edit-btn" onclick='openEditKey({{ {"name":kn,"features":k.features,"days":k.days}|tojson }})'>
                                <i class="fas fa-pen"></i> Edit
                            </button>
                            <form method="POST" action="/reseller/delete_key" style="margin:0;display:inline;" onsubmit="return confirm('Delete key {{ kn }}?');">
                                <input type="hidden" name="key_name" value="{{ kn }}">
                                <button type="submit" class="del-btn"><i class="fas fa-trash"></i> Delete</button>
                            </form>
                        </div>
                    </div>
                    {% endfor %}
                {% else %}
                    <p style="text-align:center;color:var(--muted-2);padding:30px;">No keys yet. Create your first from <b>Create API Key</b> tab.</p>
                {% endif %}
            </div>
        </section>

        <section id="sec-features" class="section">
            <div class="card">
                <div class="card-title"><i class="fas fa-cubes"></i> Available Features <span class="hint">{{ reseller_eps|length }} granted</span></div>
                {% if reseller_eps %}
                    {% for ep in reseller_eps %}
                    {% set d = endpoints[ep] %}
                    <div style="display:flex;align-items:center;gap:12px;background:var(--input-bg-2);padding:12px 14px;border-radius:11px;margin-bottom:8px;">
                        <div style="width:38px;height:38px;border-radius:10px;background:var(--red-glow);border:1px solid rgba(var(--red-r),var(--red-g),var(--red-b),.25);color:var(--red-bright);display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;">
                            <i class="{{ d.get('icon','fa-plug')|icls }}"></i>
                        </div>
                        <div style="flex:1;min-width:0;">
                            <div style="font-weight:700;font-size:14px;">{{ d.get('display_name', ep) }}</div>
                            <div style="font-size:11.5px;color:var(--muted-2);font-family:ui-monospace,monospace;margin-top:2px;">/api/{{ ep }} · param: {{ d.get('param','query') }}</div>
                        </div>
                    </div>
                    {% endfor %}
                {% else %}
                    <p style="text-align:center;color:var(--muted-2);padding:30px;">No features assigned. Contact admin.</p>
                {% endif %}
            </div>
        </section>
    </main>
</div>

<div class="modal-bg" id="editKeyModal">
    <div class="modal">
        <h3><i class="fas fa-pen-to-square"></i> Edit Key</h3>
        <div class="sub">Features aur days update karo.</div>
        <form method="POST" action="/reseller/edit_key">
            <label class="form-label">KEY NAME</label>
            <input type="text" name="edit_key_name" id="eName" class="form-control" required readonly style="cursor:not-allowed;">
            <label class="form-label">DURATION (DAYS) — MAX {{ days_left }}</label>
            <input type="number" name="edit_key_days" id="eDays" class="form-control" min="1" max="{{ days_left }}" required>
            <label class="form-label">FEATURES</label>
            <div class="rslr-picker" id="ePicker" style="max-height:220px;">
                {% for ep in reseller_eps %}
                {% set d = endpoints[ep] %}
                <label class="rslr-item" data-name="{{ ep }} {{ d.get('display_name','') }}">
                    <input type="checkbox" name="edit_key_features" value="{{ ep }}">
                    <i class="{{ d.get('icon','fa-plug')|icls }}"></i>
                    <span>{{ d.get('display_name', ep) }}</span>
                </label>
                {% endfor %}
            </div>
            <input type="hidden" name="edit_old_name" id="eOld">
            <div class="row">
                <button type="button" class="cancel" onclick="closeEditKey()">Cancel</button>
                <button type="submit" class="save"><i class="fas fa-check"></i> Save</button>
            </div>
        </form>
    </div>
</div>

<nav class="mob-nav">
    <button class="mob-tab active" data-sec="dashboard" onclick="go('dashboard')"><i class="fas fa-table-cells-large"></i>Dash</button>
    <button class="mob-tab" data-sec="create" onclick="go('create')"><i class="fas fa-plus"></i>New</button>
    <button class="mob-tab" data-sec="mykeys" onclick="go('mykeys')"><i class="fas fa-key"></i>Keys</button>
    <button class="mob-tab" data-sec="features" onclick="go('features')"><i class="fas fa-cubes"></i>Feat</button>
</nav>

<div id="toast"><i class="fas fa-check-circle"></i> <span id="toastMsg">COPIED</span></div>

<script>
function openSidebar(){document.getElementById('rslrSidebar').classList.add('open');document.getElementById('sbOverlay').classList.add('show');document.body.style.overflow='hidden';}
function closeSidebar(){document.getElementById('rslrSidebar').classList.remove('open');document.getElementById('sbOverlay').classList.remove('show');document.body.style.overflow='';}
window.addEventListener('resize', function(){ if(window.innerWidth > 900) closeSidebar(); });
function go(id){
    document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));
    document.querySelectorAll('.nav-item[data-sec]').forEach(n=>n.classList.remove('active'));
    document.querySelectorAll('.mob-tab').forEach(n=>n.classList.remove('active'));
    var sec = document.getElementById('sec-'+id); if(sec) sec.classList.add('active');
    document.querySelectorAll('[data-sec="'+id+'"]').forEach(n=>n.classList.add('active'));
    closeSidebar();
    window.scrollTo({top:0,behavior:'smooth'});
}
function toast(msg){
    var t = document.getElementById('toast');
    document.getElementById('toastMsg').textContent = msg;
    t.classList.add('show');
    clearTimeout(window.__toastT);
    window.__toastT = setTimeout(function(){ t.classList.remove('show'); }, 1600);
}
function copyText(text, msg){
    function done(){ toast(msg); }
    function fallback(){var ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();try{document.execCommand('copy');done();}catch(e){}ta.remove();}
    if(navigator.clipboard && navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(done).catch(fallback);} else { fallback(); }
}
function copyKeyVal(kn){
    var el = document.getElementById('key-' + kn); if(!el) return;
    copyText(el.textContent.trim(), 'KEY COPIED');
}
function copyLinkVal(kn){
    var el = document.getElementById('lnk-' + kn); if(!el) return;
    copyText(el.textContent.trim(), 'URL COPIED');
}
var kPicker = document.getElementById('kPicker');
var kSearch = document.getElementById('kSearch');
var kCount = document.getElementById('kCount');
function refreshKCount(){ if(kCount && kPicker) kCount.textContent = kPicker.querySelectorAll('input[type=checkbox]:checked').length; }
if(kPicker){
    kPicker.querySelectorAll('.rslr-item').forEach(function(item){
        item.addEventListener('click', function(e){
            e.preventDefault();
            var cb = item.querySelector('input');
            cb.checked = !cb.checked;
            item.classList.toggle('on', cb.checked);
            refreshKCount();
        });
    });
}
if(kSearch && kPicker){
    kSearch.addEventListener('input', function(){
        var q = this.value.trim().toLowerCase();
        kPicker.querySelectorAll('.rslr-item').forEach(function(item){
            var n = (item.dataset.name || '').toLowerCase();
            item.style.display = (!q || n.indexOf(q) !== -1) ? '' : 'none';
        });
    });
}
refreshKCount();
function keySelectAll(on){
    if(!kPicker) return;
    kPicker.querySelectorAll('.rslr-item').forEach(function(item){
        if(item.style.display === 'none') return;
        var cb = item.querySelector('input'); cb.checked = on; item.classList.toggle('on', on);
    });
    refreshKCount();
}
var ePicker = document.getElementById('ePicker');
if(ePicker){
    ePicker.querySelectorAll('.rslr-item').forEach(function(item){
        item.addEventListener('click', function(e){
            e.preventDefault();
            var cb = item.querySelector('input');
            cb.checked = !cb.checked;
            item.classList.toggle('on', cb.checked);
        });
    });
}
function openEditKey(data){
    document.getElementById('eOld').value = data.name;
    document.getElementById('eName').value = data.name;
    document.getElementById('eDays').value = data.days;
    ePicker.querySelectorAll('.rslr-item').forEach(function(item){
        var cb = item.querySelector('input');
        var on = (data.features || []).indexOf(cb.value) !== -1;
        cb.checked = on; item.classList.toggle('on', on);
    });
    document.getElementById('editKeyModal').classList.add('open');
}
function closeEditKey(){ document.getElementById('editKeyModal').classList.remove('open'); }
document.getElementById('editKeyModal').addEventListener('click', function(e){ if(e.target.id === 'editKeyModal') closeEditKey(); });
(function(){
    var h = new Date().getHours();
    var g = h<12?'Good Morning':h<17?'Good Afternoon':h<21?'Good Evening':'Good Night';
    var el = document.getElementById('greet-title');
    if(el) el.textContent = g + ', {{ reseller_name }}';
})();
</script>
""" + THEME_SCRIPT + """
</body></html>"""

# ============================================================
# ROUTES
# ============================================================
def _public_session_endpoints(db):
    pub = session.get('pub')
    if not pub:
        return None

    all_eps = {ep: d for ep, d in db["endpoints"].items()
               if not d.get("hidden") and not d.get("maintenance")}

    if pub.get('type') == 'admin':
        return all_eps

    if pub.get('type') == 'reseller':
        r = db["resellers"].get(pub.get('name'))
        if not r or not reseller_is_active(r):
            return None
        allowed = set(r.get("allowed_apis", []))
        return {ep: d for ep, d in all_eps.items() if ep in allowed}

    if pub.get('type') == 'key':
        k = db["api_keys"].get(pub.get('name'))
        if not k or not key_is_active(k):
            return None
        allowed = set(k.get("allowed_apis", []))
        return {ep: d for ep, d in all_eps.items() if ep in allowed}

    return None

@app.route('/')
def home():
    db = load_db()
    all_eps = _public_session_endpoints(db)
    if not all_eps:
        session.pop('pub', None)
        return render_template_string(PUBLIC_LOGIN_TEMPLATE,
                                      error=None,
                                      banner_image=BANNER_IMAGE,
                                      tg_link=TELEGRAM_LINK,
                                      theme_key='public_theme')

    cats = []
    for name, icon, keys in PUBLIC_CATEGORIES:
        present = [k for k in keys if k in all_eps]
        if present:
            cats.append((name, icon, present))

    extra = {ep: d for ep, d in all_eps.items() if ep not in KNOWN_PUBLIC_EP_KEYS}

    return render_template_string(PUBLIC_TEMPLATE,
                                  endpoints=all_eps,
                                  cats=cats,
                                  extra=extra,
                                  host_url=request.host_url,
                                  banner_image=BANNER_IMAGE,
                                  pub_mode=session['pub'].get('type'),
                                  pub_name=session['pub'].get('name') or '',
                                  theme_key='public_theme')

@app.route('/dashboard', methods=['GET', 'POST'])
def public_dashboard():
    db = load_db()
    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        password = (request.form.get('password') or '').strip()

        if password == ADMIN_PASSWORD and username in ['', 'admin', ADMIN_USERNAME]:
            session['pub'] = {'type': 'admin', 'name': 'admin'}
            return redirect('/')

        r = db["resellers"].get(username)
        if r and r.get("password") == password:
            if not reseller_is_active(r):
                return render_template_string(PUBLIC_LOGIN_TEMPLATE,
                                              error="Plan expired. Contact admin.",
                                              banner_image=BANNER_IMAGE,
                                              tg_link=TELEGRAM_LINK,
                                              theme_key='public_theme')
            session['pub'] = {'type': 'reseller', 'name': username}
            return redirect('/')

        if username in db["api_keys"] and password == ADMIN_PASSWORD:
            if not key_is_active(db["api_keys"][username]):
                return render_template_string(PUBLIC_LOGIN_TEMPLATE,
                                              error="API key expired.",
                                              banner_image=BANNER_IMAGE,
                                              tg_link=TELEGRAM_LINK,
                                              theme_key='public_theme')
            session['pub'] = {'type': 'key', 'name': username}
            return redirect('/')

        return render_template_string(PUBLIC_LOGIN_TEMPLATE,
                                      error="Invalid username or password!",
                                      banner_image=BANNER_IMAGE,
                                      tg_link=TELEGRAM_LINK,
                                      theme_key='public_theme')

    return redirect('/')

@app.route('/pub/logout')
def public_logout():
    session.pop('pub', None)
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        p = request.form.get('password') or ''
        if p == ADMIN_PASSWORD:
            session['admin'] = True; session['username'] = ADMIN_USERNAME
            return redirect('/admin')
        error_message = "Invalid Password!"
    return render_template_string(ADMIN_TEMPLATE, logged_in=False,
                                  error_msg=error_message, tg_link=TELEGRAM_LINK,
                                  icon_choices=ICON_CHOICES,
                                  banner_image=BANNER_IMAGE,
                                  brand_icons=sorted(BRAND_ICONS),
                                  auto_icons_json=json.dumps(AUTO_ICON_MAP),
                                  theme_key='admin_theme')

def _render_admin():
    db = load_db()
    keys = get_keys_and_reset(db)
    a = db["analytics"]
    if a.get("today_date") != str(date.today()):
        a["today_date"] = str(date.today()); a["today_calls"] = 0; save_db(db)

    resellers_view = {}
    active_resellers = 0
    for rn, r in db["resellers"].items():
        d_left = reseller_days_left(r)
        is_act = reseller_is_active(r)
        if is_act: active_resellers += 1
        resellers_view[rn] = {
            "password": r.get("password", ""),
            "allowed_apis": r.get("allowed_apis", []),
            "duration_days": r.get("duration_days", 30),
            "expires_at": r.get("expires_at", ""),
            "notes": r.get("notes", ""),
            "device_locked": bool(r.get("device_token")),
            "is_active": is_act,
            "days_left": d_left,
            "my_keys_count": len(r.get("my_keys", {})),
        }

    return render_template_string(
        ADMIN_TEMPLATE, logged_in=True, keys=keys,
        key_active={k: key_is_active(v) for k, v in keys.items()},
        total_keys=len(keys),
        active_keys=sum(1 for v in keys.values() if key_is_active(v)),
        total_calls=a.get("total_requests", 0),
        today_calls=a.get("today_calls", 0),
        endpoints=visible_endpoints(db),
        resellers=resellers_view,
        total_resellers=len(resellers_view),
        active_resellers=active_resellers,
        tg_link=TELEGRAM_LINK,
        icon_choices=ICON_CHOICES,
        banner_image=BANNER_IMAGE,
        brand_icons=sorted(BRAND_ICONS),
        auto_icons_json=json.dumps(AUTO_ICON_MAP),
        theme_key='admin_theme')

@app.route('/admin')
@admin_required
def admin_panel(): return _render_admin()

@app.route('/logout')
def logout():
    session.clear(); return redirect('/login')

@app.route('/change_password', methods=['POST'])
@admin_required
def change_password():
    global ADMIN_PASSWORD
    if request.form.get('old_pass') == ADMIN_PASSWORD and request.form.get('auth_key') == SECRET_AUTH_KEY:
        ADMIN_PASSWORD = request.form.get('new_pass')
        return "<script>alert('Password Changed!');location.href='/logout';</script>"
    return "<script>alert('Invalid Credentials!');location.href='/admin';</script>"

@app.route('/generate', methods=['POST'])
@admin_required
def generate_key():
    db = load_db()
    mode = request.form.get('expiry_mode', 'hours')
    if mode == 'hours':
        try: h = int(request.form.get('hours') or 24)
        except: h = 24
        expiry_dt = datetime.now() + timedelta(hours=max(1, h))
    elif mode == 'days':
        try: d = int(request.form.get('days') or 30)
        except: d = 30
        expiry_dt = datetime.now() + timedelta(days=max(1, d))
    else:
        ds = request.form.get('expiry_date') or ''
        try: expiry_dt = datetime.strptime(ds, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        except Exception: expiry_dt = datetime.now() + timedelta(days=30)
    key_name = (request.form.get('key_name') or '').strip()
    if key_name:
        db["api_keys"][key_name] = {
            "limit": int(request.form.get('limit') or 0), "used": 0,
            "expiry_date": expiry_dt.strftime('%Y-%m-%d %H:%M:%S'),
            "allowed_apis": request.form.getlist('allowed_apis'),
            "last_used_date": str(date.today())}
        save_db(db)
    return redirect('/admin')

@app.route('/edit_key', methods=['POST'])
@admin_required
def edit_key():
    db = load_db()
    old_name = (request.form.get('old_name') or '').strip()
    new_name = (request.form.get('new_name') or '').strip()
    if not old_name or old_name not in db["api_keys"]: return redirect('/admin')
    entry = db["api_keys"][old_name]
    entry["limit"] = int(request.form.get('new_limit') or 0)
    entry["expiry_date"] = (request.form.get('new_expiry') or entry.get('expiry_date') or '').strip()
    entry["allowed_apis"] = request.form.getlist('new_allowed')
    if new_name and new_name != old_name:
        if new_name in db["api_keys"]:
            entry["used"] = max(entry.get("used", 0), db["api_keys"][new_name].get("used", 0))
        db["api_keys"].pop(old_name, None); db["api_keys"][new_name] = entry
    else:
        db["api_keys"][old_name] = entry
    save_db(db); return redirect('/admin')

@app.route('/delete_key', methods=['POST'])
@admin_required
def delete_key():
    db = load_db(); db["api_keys"].pop(request.form.get('key_name'), None)
    save_db(db); return redirect('/admin')

@app.route('/add_feature', methods=['POST'])
@admin_required
def add_feature():
    ep = (request.form.get('ep_name') or '').strip().replace(" ", "").replace("/", "")
    display = (request.form.get('ep_display') or '').strip() or ep
    param = (request.form.get('ep_param') or '').strip() or 'query'
    icon = (request.form.get('ep_icon') or '').strip()
    url = (request.form.get('ep_url') or '').strip()
    maint = (request.form.get('ep_maint') == 'on')
    if not ep: return redirect('/admin')
    if not icon: icon = auto_icon_for(display) or auto_icon_for(ep) or 'fa-plug'
    icon = normalize_icon(icon)
    db = load_db()
    if ep in db["endpoints"] and not db["endpoints"][ep].get("hidden"):
        d = db["endpoints"][ep]
        d["display_name"] = display; d["param"] = param; d["icon"] = icon
        d["maintenance"] = maint
        if url: d["url"] = url
        save_db(db); return redirect('/admin')
    db["endpoints"][ep] = {"url": url, "maintenance": maint,
        "is_custom": ep not in STANDARD_APIS,
        "display_name": display, "param": param, "icon": icon, "hidden": False}
    save_db(db); return redirect('/admin')

@app.route('/edit_feature', methods=['POST'])
@admin_required
def edit_feature():
    db = load_db()
    old_ep = (request.form.get('old_ep') or '').strip()
    if not old_ep or old_ep not in db["endpoints"]: return redirect('/admin')
    new_ep = (request.form.get('new_ep') or old_ep).strip().replace(" ", "").replace("/", "")
    d = db["endpoints"][old_ep]
    d["display_name"] = (request.form.get('new_display') or '').strip() or new_ep
    d["param"] = (request.form.get('new_param') or '').strip() or 'query'
    icon = (request.form.get('new_icon') or '').strip()
    d["icon"] = normalize_icon(icon) if icon else d.get("icon", 'fa-plug')
    d["url"] = (request.form.get('new_url') or '').strip()
    d["maintenance"] = (request.form.get('new_maint') == 'on')
    d["hidden"] = False
    if new_ep and new_ep != old_ep:
        db["endpoints"].pop(new_ep, None); db["endpoints"].pop(old_ep, None); db["endpoints"][new_ep] = d
    else:
        db["endpoints"][old_ep] = d
    save_db(db); return redirect('/admin')

@app.route('/delete_feature', methods=['POST'])
@admin_required
def delete_feature():
    ep = (request.form.get('ep_name') or '').strip()
    if not ep: return redirect('/admin')
    db = load_db()
    if ep in db["endpoints"]:
        if db["endpoints"][ep].get("is_custom"): db["endpoints"].pop(ep, None)
        else: db["endpoints"][ep]["hidden"] = True
    save_db(db); return redirect('/admin')

@app.route('/add_reseller', methods=['POST'])
@admin_required
def add_reseller():
    username = (request.form.get('rslr_username') or '').strip()
    password = (request.form.get('rslr_password') or '').strip()
    try: days = int(request.form.get('rslr_days') or 30)
    except: days = 30
    days = max(1, min(3650, days))
    features = request.form.getlist('rslr_features')
    notes = (request.form.get('rslr_notes') or '').strip()
    if not username or not password: return redirect('/admin')
    db = load_db()
    if username in db["resellers"]: return redirect('/admin')
    now = datetime.now()
    db["resellers"][username] = {
        "password": password,
        "allowed_apis": features,
        "created_at": now.strftime('%Y-%m-%d %H:%M:%S'),
        "expires_at": (now + timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S'),
        "duration_days": days,
        "active": True,
        "device_token": None,
        "calls_used": 0,
        "notes": notes,
        "my_keys": {},
    }
    save_db(db); return redirect('/admin')

@app.route('/edit_reseller', methods=['POST'])
@admin_required
def edit_reseller():
    db = load_db()
    old_name = (request.form.get('rslr_old_username') or '').strip()
    if not old_name or old_name not in db["resellers"]: return redirect('/admin')
    r = db["resellers"][old_name]
    new_name = (request.form.get('rslr_new_username') or old_name).strip() or old_name
    new_pass = (request.form.get('rslr_new_password') or '').strip()
    if new_pass: r["password"] = new_pass
    try: days = int(request.form.get('rslr_new_days') or r.get("duration_days", 30))
    except: days = r.get("duration_days", 30)
    days = max(1, min(3650, days))
    r["duration_days"] = days
    now = datetime.now()
    r["expires_at"] = (now + timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
    r["allowed_apis"] = request.form.getlist('rslr_new_features')
    r["notes"] = (request.form.get('rslr_new_notes') or '').strip()
    if new_name != old_name:
        if new_name in db["resellers"]: return redirect('/admin')
        db["resellers"].pop(old_name, None); db["resellers"][new_name] = r
    else:
        db["resellers"][old_name] = r
    save_db(db); return redirect('/admin')

@app.route('/delete_reseller', methods=['POST'])
@admin_required
def delete_reseller():
    db = load_db(); db["resellers"].pop(request.form.get('rslr_username'), None)
    save_db(db); return redirect('/admin')

@app.route('/reset_reseller_device', methods=['POST'])
@admin_required
def reset_reseller_device():
    db = load_db()
    rn = (request.form.get('rslr_username') or '').strip()
    if rn in db["resellers"]:
        db["resellers"][rn]["device_token"] = None
        save_db(db)
    return redirect('/admin')

@app.route('/save_maintenance', methods=['POST'])
@admin_required
def save_maintenance():
    db = load_db()
    for ep in list(db["endpoints"].keys()):
        db["endpoints"][ep]["maintenance"] = (request.form.get(f'maint_{ep}') == 'on')
    save_db(db); return redirect('/admin')

# ============================================================
# RESELLER SESSION
# ============================================================
@app.route('/reseller', methods=['GET', 'POST'])
def reseller_login():
    if request.method == 'GET':
        if session.get('reseller'): return redirect('/reseller/panel')
        return render_template_string(RESELLER_LOGIN_TEMPLATE, error=None,
                                      banner_image=BANNER_IMAGE, tg_link=TELEGRAM_LINK,
                                      theme_key='reseller_theme')
    username = (request.form.get('username') or '').strip()
    password = (request.form.get('password') or '').strip()
    db = load_db()
    r = db["resellers"].get(username)
    if not r or r.get("password") != password:
        return render_template_string(RESELLER_LOGIN_TEMPLATE, error="Invalid username or password!",
                                      banner_image=BANNER_IMAGE, tg_link=TELEGRAM_LINK,
                                      theme_key='reseller_theme')
    if not reseller_is_active(r):
        return render_template_string(RESELLER_EXPIRED_TEMPLATE,
                                      banner_image=BANNER_IMAGE, tg_link=TELEGRAM_LINK,
                                      theme_key='reseller_theme')
    existing_token = r.get("device_token")
    cookie_token = request.cookies.get('rslr_dt')
    if existing_token:
        if not cookie_token or cookie_token != existing_token:
            return render_template_string(RESELLER_LOGIN_TEMPLATE,
                                          error="Already logged in on another device. Contact admin to reset.",
                                          banner_image=BANNER_IMAGE, tg_link=TELEGRAM_LINK,
                                          theme_key='reseller_theme')
        new_token = existing_token
    else:
        new_token = gen_device_token()
        db["resellers"][username]["device_token"] = new_token
        save_db(db)
    session['reseller'] = username
    resp = make_response(redirect('/reseller/panel'))
    resp.set_cookie('rslr_dt', new_token, max_age=60*60*24*365, httponly=True, samesite='Lax')
    return resp

@app.route('/reseller/logout')
def reseller_logout():
    session.pop('reseller', None)
    return redirect('/reseller')

@app.route('/reseller/panel')
def reseller_panel():
    rname = session.get('reseller')
    if not rname: return redirect('/reseller')
    db = load_db()
    r = db["resellers"].get(rname)
    if not r:
        session.pop('reseller', None); return redirect('/reseller')
    if not reseller_is_active(r):
        session.pop('reseller', None)
        return render_template_string(RESELLER_EXPIRED_TEMPLATE,
                                      banner_image=BANNER_IMAGE, tg_link=TELEGRAM_LINK,
                                      theme_key='reseller_theme')
    dev_token = r.get("device_token")
    if dev_token and request.cookies.get('rslr_dt') != dev_token:
        session.pop('reseller', None); return redirect('/reseller')

    all_eps = visible_endpoints(db)
    allowed = [ep for ep in r.get("allowed_apis", []) if ep in all_eps]
    expires_dt = parse_expiry(r.get("expires_at"))

    host = request.host_url.rstrip('/')
    raw_my_keys = r.get("my_keys", {}) or {}
    my_keys_view = {}
    for kn, k in raw_my_keys.items():
        feats = k.get("features", [])
        sample_link = ""
        if feats:
            first_ep = feats[0]
            pname = all_eps.get(first_ep, {}).get("param", "query") if first_ep in all_eps else "query"
            sample_link = f"{host}/api/{first_ep}?key={k.get('api_key','')}&{pname}=YOUR_VALUE"
        else:
            sample_link = f"{host}/api/<endpoint>?key={k.get('api_key','')}&param=YOUR_VALUE"

        my_keys_view[kn] = {
            "api_key": k.get("api_key", ""),
            "features": feats,
            "features_count": len(feats),
            "days": k.get("days", 0),
            "expires_display": parse_expiry(k.get("expires_at")).strftime('%d %b %Y'),
            "calls_used": k.get("calls_used", 0),
            "is_active": subkey_is_active(k),
            "sample_link": sample_link,
        }

    return render_template_string(
        RESELLER_PANEL_TEMPLATE,
        reseller_name=rname,
        reseller_eps=allowed,
        my_keys=my_keys_view,
        endpoints=all_eps,
        days_left=reseller_days_left(r),
        calls_used=r.get("calls_used", 0),
        expires_display=expires_dt.strftime('%d %b %Y'),
        host_url=request.host_url,
        banner_image=BANNER_IMAGE,
        icon_choices=ICON_CHOICES,
        brand_icons=sorted(BRAND_ICONS),
        auto_icons_json=json.dumps(AUTO_ICON_MAP),
        tg_link=TELEGRAM_LINK,
        theme_key='reseller_theme')

@app.route('/reseller/create_key', methods=['POST'])
def reseller_create_key():
    rname = session.get('reseller')
    if not rname: return redirect('/reseller')
    db = load_db()
    r = db["resellers"].get(rname)
    if not r or not reseller_is_active(r): return redirect('/reseller/panel')

    kn = (request.form.get('key_name') or '').strip().replace(" ", "_")
    if not kn: return redirect('/reseller/panel')
    try: days = int(request.form.get('key_days') or 1)
    except: days = 1

    max_days = reseller_days_left(r)
    if max_days <= 0: return redirect('/reseller/panel')
    days = max(1, min(days, max_days))

    allowed_set = set(r.get("allowed_apis", []))
    picked = [f for f in request.form.getlist('key_features') if f in allowed_set]
    if not picked: return redirect('/reseller/panel')

    full_kn = f"{rname}_{kn}"
    suffix = secrets.token_hex(3)
    api_key_val = f"{full_kn}_{suffix}"

    now = datetime.now()
    r.setdefault("my_keys", {})
    r["my_keys"][full_kn] = {
        "api_key": api_key_val,
        "features": picked,
        "days": days,
        "created_at": now.strftime('%Y-%m-%d %H:%M:%S'),
        "expires_at": (now + timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S'),
        "calls_used": 0,
    }
    save_db(db)
    return redirect('/reseller/panel')

@app.route('/reseller/edit_key', methods=['POST'])
def reseller_edit_key():
    rname = session.get('reseller')
    if not rname: return redirect('/reseller')
    db = load_db()
    r = db["resellers"].get(rname)
    if not r or not reseller_is_active(r): return redirect('/reseller/panel')

    old_kn = (request.form.get('edit_old_name') or '').strip()
    my_keys = r.get("my_keys", {}) or {}
    if old_kn not in my_keys: return redirect('/reseller/panel')

    try: days = int(request.form.get('edit_key_days') or 1)
    except: days = 1
    max_days = reseller_days_left(r)
    days = max(1, min(days, max_days if max_days > 0 else 1))

    allowed_set = set(r.get("allowed_apis", []))
    picked = [f for f in request.form.getlist('edit_key_features') if f in allowed_set]
    if not picked: picked = my_keys[old_kn].get("features", [])

    k = my_keys[old_kn]
    k["features"] = picked
    k["days"] = days
    k["expires_at"] = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
    save_db(db)
    return redirect('/reseller/panel')

@app.route('/reseller/delete_key', methods=['POST'])
def reseller_delete_key():
    rname = session.get('reseller')
    if not rname: return redirect('/reseller')
    db = load_db()
    r = db["resellers"].get(rname)
    if not r: return redirect('/reseller/panel')
    kn = (request.form.get('key_name') or '').strip()
    if kn in r.get("my_keys", {}):
        r["my_keys"].pop(kn, None)
        save_db(db)
    return redirect('/reseller/panel')

# ============================================================
# API
# ============================================================
@app.route('/api/<api_type>', methods=['GET'])
def dynamic_api(api_type):
    db = load_db()
    d = db["endpoints"].get(api_type)
    if not d or d.get("hidden"):
        return jsonify({"error": "Invalid Endpoint"}), 404
    if d.get("maintenance"):
        return jsonify({"error": "Under Maintenance, try again later!", "developer": TELEGRAM_LINK}), 503

    api_key = request.args.get('key')
    if not api_key:
        return jsonify({"error": "Missing API key"}), 400

    param_name = None
    owner_type = None
    owner_name = None
    sub_key_name = None

    key_info = db["api_keys"].get(api_key)
    if key_info:
        if api_type not in key_info.get("allowed_apis", []):
            return jsonify({"error": "Not Permitted for this API"}), 403
        if parse_expiry(key_info.get('expiry_date')) <= datetime.now():
            return jsonify({"error": "Key Expired"}), 403
        if key_info['limit'] != 0 and key_info['used'] >= key_info['limit']:
            return jsonify({"error": "Limit Reached"}), 429
        owner_type = "admin"; owner_name = api_key
        param_name = d.get("param", "query")
    else:
        sub_match = None
        for rn, r in db["resellers"].items():
            for kn, k in (r.get("my_keys") or {}).items():
                if k.get("api_key") == api_key:
                    sub_match = (rn, r, kn, k); break
            if sub_match: break
        if not sub_match:
            return jsonify({"error": "Invalid Key"}), 401
        rn, r, kn, k = sub_match
        if not reseller_is_active(r):
            return jsonify({"error": "Reseller plan expired. Contact admin.", "contact": TELEGRAM_LINK}), 403
        if not subkey_is_active(k):
            return jsonify({"error": "This key has expired. Contact reseller."}), 403
        if api_type not in k.get("features", []):
            return jsonify({"error": "Not Permitted for this API"}), 403
        owner_type = "reseller"; owner_name = rn; sub_key_name = kn
        param_name = d.get("param", "query")

    query_val = request.args.get(param_name)
    if not query_val:
        return jsonify({"error": f"Missing param: {param_name}"}), 400

    base_url = d.get("url", "")
    if not base_url:
        return jsonify({"error": "Backend URL not configured. Contact admin."}), 500

    try:
        resp = requests.get(base_url + query_val, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code == 200:
            try: raw = resp.json()
            except Exception: raw = {"result": resp.text}
            data = raw if isinstance(raw, dict) else {"result": raw}
            data = clean_response(data)
            data['credit'] = "@Hindustanhack"
            if owner_type == "admin":
                db["api_keys"][owner_name]["used"] = db["api_keys"][owner_name].get("used", 0) + 1
            else:
                db["resellers"][owner_name]["calls_used"] = db["resellers"][owner_name].get("calls_used", 0) + 1
                if sub_key_name:
                    sk = db["resellers"][owner_name].get("my_keys", {}).get(sub_key_name)
                    if sk: sk["calls_used"] = sk.get("calls_used", 0) + 1
            bump_analytics(db, api_type); save_db(db)
            return jsonify(data)
        return jsonify({"error": f"Original API Down ({resp.status_code})"}), 502
    except requests.exceptions.Timeout:
        return jsonify({"error": "Original API Timeout"}), 504
    except Exception:
        return jsonify({"error": "Original API Unreachable"}), 504

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("HINDUSTAN OSINT")
    print("PUBLIC   : http://127.0.0.1:8080/  (login required)")
    print("ADMIN    : http://127.0.0.1:8080/login")
    print("RESELLER : http://127.0.0.1:8080/reseller")
    print("=" * 50 + "\n")
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)