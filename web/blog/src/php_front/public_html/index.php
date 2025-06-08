<?php

    session_start();

    $redis = new Redis();
    $redis->connect('redis', 6379);

    $request_limit = 10;
    $time_limit = 5;
    $total_requests = 0;
    $timeout = 60;

    $user_ip_address = $_SERVER['REMOTE_ADDR'];

    if (!$redis->exists($user_ip_address)) {
        $redis->set($user_ip_address, 1);
        $redis->expire($user_ip_address, $time_limit);
    } else {
        $total_requests = $redis->get($user_ip_address);
        if ($total_requests < 0) {
            echo "<pre>Stop spamming my website, you hacker! You got time out!</pre>";
            die();
        }
        $redis->INCR($user_ip_address);
        $total_requests = $redis->get($user_ip_address);
        if ($total_requests > $request_limit) {
            $redis->set($user_ip_address, -1);
            $redis->expire($user_ip_address, $timeout);
            echo "<pre>Stop spamming my website, you hacker! You got time out!</pre>";
            die();
        }
    }

?>

<html>
    
    <head>
        <title>Villain's Blog</title>
        <link href="https://fonts.googleapis.com/css2?family=Jim+Nightshade&display=swap" rel="stylesheet">
        <style>     

            body{
                width: 99vw;
                color: white;
                display: flex;
                flex-direction: column;
                align-items: center;
                overflow-x: hidden;
                font-family:'Jim Nightshade';
                font-size: x-large;
                height: max-content;
                background: linear-gradient(0deg, rgb(32, 2, 0) 0%,  rgb(0, 0, 0)100%);
                
            }

            h1,h2,h3{
                color: red;
            }

            a{
                cursor: pointer;
                color: #dd0;
                text-shadow:none;
            }

            i{
                color: red;
                text-align: right;
                font-size: xx-large;  
            }
            img{
                width: 17vw;
                transition: all 0.3s ease; 
                filter: brightness(100%);
                transition: all 0.3s ease;  
            }


            img:hover{
                filter: brightness(100%) drop-shadow(0 0 15px rgba(255, 0, 0, 0.8));
                cursor: pointer;
                scale:0.9;
            }

            .header{
                display: flex;
                flex-direction: column;
                width: 50%;
                justify-content: center;
                align-items: center;
                
            }

            .blog-entry{
                display: flex;
                flex-direction: column;
                text-align: center; 
                
            }

            .blog-entry h2{
                color: red;
                text-shadow: 0 0 10px red;
            }

            .blog-entry p{
                text-align: left;
            }

            .blog-entry button {
                width: 11vw;
                justify-content: center;
                align-items: center;
                display: flex;
                flex-direction: column;
                margin: auto;
                background: transparent;
                color: red;
                border-radius: 50px;
                font-family: 'Jim Nightshade';
                border-style: ridge;
                font-size: xx-large;
                border: 2px solid red;
                transition: background 0.3s ease, box-shadow 0.3s ease, color 0.3s ease;
                margin-top: 3vh;
            }

            .blog-entry button:hover {
                background: red;
                color: black;
                box-shadow: 0 0 15px 5px red; /* Glow effect */
                cursor: pointer;
            }

            .content{
                position: absolute;
                top: 0; 
                left: 0; 
                width: 100%;
                background: black; 
                z-index: 9999;
                display: flex;  
                flex-direction: column;
                /* background: #0000004f; */
                padding: 0 0 5% 0;
            }
            .text-blog{
                border-style: outset;
                border-color: #640202;
                border-radius: 50px;
                margin: 0 5%;
                padding: 3% 5%;
            }

            .signature{
                width: 75vw;
                text-align: right;
            }
            #blog{
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 3%
            }
        </style>
    </head>
    <body id="body">
        <div class="header">
            <h1>Welcome to villain's blog</h1>
            <p>You are a villain, and you have things to say? Then you are at the right place! In this page you can read other member's blogs, and feel free to contact <b>Sylvester</b> if you want to get your own account ;)</p>
        </div>
        <div id="blog"></div>
        <div id="image"><img src="eyes.png"></div>
    </body>
    <script>
        async function get_blog(blog="all") {
            let reponse = await fetch('/blog.php?blog='+blog);
            let json = await reponse.json();
            document.getElementById('blog').innerHTML = "";
            if (blog == "all") {
                for (let i = 0; i < json.length; i++) {
                    var elemDiv = document.createElement('div');
                    elemDiv.className = "blog-entry";
                    elemDiv.innerHTML = `<h2><a onclick="get_blog(blog=${json[i].id})">${json[i].title}</a> - <i>${json[i].name}</i></h2>`;
                    document.getElementById('blog').appendChild(elemDiv);
                }
            } else {
                var elemDiv = document.createElement('div');
                elemDiv.className = "blog-entry";
                elemDiv.innerHTML = `<div class="content"><h2>${json.title}</h2><div class="text-blog"><p>${json.content}</p><div class="signature"><i>- ${json.name}</i></div></div><button onclick="get_blog();">Back</button></div>`;
                document.getElementById('blog').appendChild(elemDiv);
            }
        }
        get_blog();
    </script>
</html>