
const allTags = ["Arts and Entertainment",
"Autos and Vehicles",
"Beauty and Fitness",
"Books and Literature",
"Business and Industry",
"Career and Education",
"Computer and electronics",
"Finance",
"Food and Drink",
"Gambling",
"Games",
"Health",
"Home and Garden",
"Internet and Telecom",
"Law and Government",
"News and Media",
"People and Society",
"Pets and Animals",
"Recreation and Hobbies",
"Reference",
"Science",
"Shopping",
"Sports",
"Travel",
"Adult"]


const allowedTags = [
"Books and Literature",
"Career and Education",
"Computer and electronics",
"Health",
"Internet and Telecom",
"Law and Government",
"News and Media",
"Reference",
"Science",]

const skipDomain = ["www.google.com",
"www.google.co.in",
"google.co.in",
"google.com",
"chrome",
]


const youtubeAllowedtag = [
    "Music"
    ,"News & Politics"
    ,"Education"
    ,"Science & Technology"]


function post(url){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.send();
}

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false );
    xmlHttp.send();
    return xmlHttp.responseText;
}

function handle_youtube(url)
{
    const result = url.split("v=")[1]
    if(!result)
    {
        const url = decodeURIComponent('http://localhost:3001/website?domain=youtube.com&bool=true')   
        post(url)
        return;
    }   
    
    const res = httpGet("https://www.googleapis.com/youtube/v3/videos?part=snippet&id="+result+"&key=AIzaSyAa_7dOv2a4wNBtImGiI58sIyNhPoehPwk&type=video")

    const resJSON = JSON.parse(res)
    // console.log(resJSON)    
    const title = resJSON.items[0].snippet.title
    const catId = resJSON.items[0].snippet.categoryId

    const catRes = httpGet("https://www.googleapis.com/youtube/v3/videoCategories?key=AIzaSyAa_7dOv2a4wNBtImGiI58sIyNhPoehPwk&part=snippet&id="+catId)

    const catJSON = JSON.parse(catRes)
    const cat = catJSON.items[0].snippet.title

    if(youtubeAllowedtag.includes(cat))
    {
        const youtubeUrl = decodeURIComponent('http://localhost:3001/youtube?title='+title+'&bool='+true)
        post(youtubeUrl)
        return
    }
    
    const youtubeUrl = decodeURIComponent('http://localhost:3001/youtube?title='+title+'&bool='+false)  
    post(youtubeUrl)
    return

    // console.log()

}

function check(url)
{
    var domain = url.replace('http://','').replace('https://','').split(/[/?#]/)[0];

    if(domain == "youtube.com" || domain == "www.youtube.com")
    {
        handle_youtube(url)
        return;
    }
    console.log(domain)

    if(skipDomain.includes(domain))
    {
        console.log("Skipped")
        return
    }
        
    fetch("https://website-categorization-api.whoisxmlapi.com/api/v1?apiKey=at_w5oS9FmRsWooaojsNunHpF6G1lAuu&domainName="+encodeURI(domain)).then((res)=>{
        return res.json()
    }).then((data)=>{

        const cat = data['categories']

        var ok = true;

        cat.forEach(element => {
            if(!allowedTags.includes(element))
            {
                ok=false;
                return;
             }
         });

        console.log(domain)
        // console.log(cat)
        console.log(ok)

        const url = decodeURIComponent('http://localhost:3001/website?domain='+domain+'&bool='+ok)   
        post(url)

           
        // fetch(decodeURIComponent('https://localhost:3001/website?domain=youtube.com&bool='+ok))


    }).catch((e)=>{
        console.log(e)
        return
    })
}


chrome.tabs.onUpdated.addListener(function(tabId,changeInfo,tab) {
    if(changeInfo.url)
    {
        // alert(changeInfo.url)
        check(changeInfo.url)
        console.log(changeInfo) 
    }
});

chrome.tabs.onActivated.addListener(function(){
    chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
    if(tabs[0])
    {
        var url = tabs[0]['url']
        // check(url)
        console.log(url)
    }
})
})
