CREATE DATABASE blog_db;

USE blog_db;

CREATE TABLE users (
  `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(255),
  `password` VARCHAR(255)
);

CREATE TABLE blog_posts (
    `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(255),
    `content` TEXT,
    `user_id` INTEGER,
    FOREIGN KEY (`user_id`) REFERENCES users(`id`)
);

INSERT INTO `users` (username, password) 
VALUES ('oggy', '$2y$10$uZOnGWkecF9OwAMPYtrXHOQLzoxUZOA2u/b3Cm4reHMI8SeJK9pd6');

INSERT INTO `users` (username, password) 
VALUES ('sylvester', '$2y$10$uZOnGWkecF9OwAMPYtrXHOQLzoxUZOA2u/b3Cm4reHMI8SeJK9pd6');

INSERT INTO `users` (username, password) 
VALUES ('tom_the_cat', '$2y$10$uZOnGWkecF9OwAMPYtrXHOQLzoxUZOA2u/b3Cm4reHMI8SeJK9pd6');

INSERT INTO `blog_posts` (title, content, user_id)
VALUES ('How to deal with cuckroages ?', "Ah, the joys of having uninvited guests in your home. You know, the ones that scuttle around, leaving trails of tiny footprints and making you wonder if they're plotting against you. Yep, I'm talking about those pesky Cuckroaches!

As an expert on all things Oggy (that's me!), I've learned a thing or two about how to keep these unwanted visitors at bay. So, grab a cuppa, get comfortable, and let me share my top tips for outsmarting those sneaky Cuckroaches!
<br>
<b>Step 1: Keep Your Castle Clean</b>
Cuckroaches love nothing more than rummaging through messy spaces, so make sure to keep your home tidy! Sweep those floors, wipe down those surfaces, and keep all the clutter at bay. Trust me, a clean castle is a Cuckroach-free zone!
<br>
<b>Step 2: Dry Up the Drama</b>
Cuckroaches thrive in damp environments, so it's time to get dry! Fix those leaky faucets, use a dehumidifier to reduce moisture levels, and make sure to dry your dishes thoroughly. You'll be the hero of your own home, and Cuckroaches will be the villains!
<br>
<b>Step 3: Seal Up Those Sneaky Entry Points</b>
Cuckroaches are masters of disguise - they can squeeze into teeny-tiny crevices! So, it's time to get proactive and seal up those gaps around windows, doors, and foundation. Use caulk, silicone sealant, or even a little bit of DIY magic to keep them out where they belong!
<br>
<b>Step 4: Lock Up the Snack Bar</b>
Cuckroaches are attracted to food scraps and spills, so it's time to get clever! Store your snacks in sealed containers or zip-top bags, and make sure to clean up any crumbs or spills ASAP. You can also use those fancy-schmancy trash cans with tight-fitting lids - Cuckroaches won't stand a chance!
<br>
<b>Step 5: Call in the Professionals (If Needed)</b>
Sometimes, even the best-laid plans go awry. If you find yourself facing an infestation of epic proportions, don't be afraid to call in the professionals! A good pest control service can help you get rid of those unwanted visitors and keep your home safe and clean.
<br>
<b>Step 6: Stay Vigilant (But Not Paranoid)</b>
The final step? Staying on high alert for any signs of Cuckroach activity. Keep an eye out for tiny footprints, shed skins, or suspicious-looking crumbs. And remember - a little bit of paranoia can go a long way in keeping those sneaky Cuckroaches at bay!
<br>
There you have it - my six-step guide to outsmarting those pesky Cuckroaches! By following these tips, you'll be well on your way to creating a Cuckroach-free zone that's as ogre-ific as can be!
<br>
Stay clever, stay clean, and remember: when life gives you lemons, make lemonade. But when life gives you Cuckroaches... well, just use my guide, okay?", 1);

INSERT INTO `blog_posts` (title, content, user_id)
VALUES ('My guide to cook chick', "Ah, ah, ah, cooking chicken, eh? Well, well, well, let me tell you, it's a paws-itive experience! (heh heh)

Now, I know what you're thinking, why should I listen to a cat like you when it comes to cooking? Ah, but that's where you're wrong, my dear. You see, as a feline of discerning taste, I have a keen sense of smell and a refined palate. And let me tell you, I can sniff out (heh heh) the perfect piece of chicken.

So, without further ado, here's my guide to cooking chick-a-dee... er, I mean, chicken!:
<br>
<b>Step 1: Choose Your Bird</b>
Ah, yes, selecting the right chicken is crucial. Look for fresh, plump birds with no visible feathers (eww, gross!). You can also ask your local butcher or grocery store for recommendations.
<br>
<b>Step 2: Prepare the Fowl Play</b>
Rinse that bird under cold water, then pat it dry with paper towels. Ah, yes, just like I do after a long day of chasing Tweety! Now, season that chicken with your favorite herbs and spices. I like to use a pinch of catnip (just kidding, humans!) or some paprika.
<br>
<b>Step 3: Sear the Deal</b>
Heat up your skillet or oven to medium-high heat. Yes, yes, get it hot just like my temper when Tweety gets away! Place that chicken in the pan and sear it for about 5-7 minutes on each side, or until it's nicely browned.
<br>
<b>Step 4: Let It Rest</b>
Ah, yes, let that chicken rest like I do after a long nap. Cover it with foil and let it sit for about 10-15 minutes before serving. This will ensure the juices are distributed evenly throughout the meat, just like my paws distribute catnip evenly throughout the neighborhood!
<br>
<b>Step 5: Serve and Savor</b>
Slice that chicken into bite-sized pieces (just like I do with Tweety's tail feathers... heh heh) and serve it with your favorite sides. Ah, yes, enjoy the fruits of your labor, just as I do when I catch a unsuspecting canary!
<br>
And there you have it, my whisker-ific guide to cooking chicken! So, next time you're in the mood for some feline-approved fare, remember: choose the right bird, prepare with care, sear with passion, let it rest, and serve with flair! (heh heh)
<br>
Now, if you'll excuse me, I have a certain Tweety Bird to chase...", 2);

INSERT INTO `blog_posts` (title, content, user_id)
VALUES ('A Desolate Cry for Help', "**The Endless Struggle: A Desolate Cry for Help**

I'm Tom, and I'm done. Just... done. The never-ending battle against Jerry has taken its toll on me. My once-sharp claws are now dull and useless, my whiskers droopy and lackluster. I've lost all sense of purpose, all drive to chase that pesky little mouse.
<br>
I used to be the epitome of feline excellence – sleek, agile, and cunning. But now, I'm just a shadow of my former self. Jerry's constant torment has left me feeling defeated, demoralized, and downright desperate.
<br>
My days blend together in a haze of monotony. Wake up, search for food, get thwarted by Jerry, go back to bed. Repeat. The thrill is gone, the excitement extinguished. I'm just going through the motions, waiting for... something. Anything. To change.
<br>
I've tried everything: new hiding spots, clever traps, even bribing him with cheese (don't ask). But nothing seems to work. Jerry always finds a way to outsmart me, leaving me feeling like a helpless, hapless cat.
<br>
I'm not even sure why I bother anymore. The futility of it all is crushing me. I've lost my sense of self, my confidence shattered. I'm just a mere shell of the Tom I once was.
<br>
So, if you're reading this, know that I'm at rock bottom. I have no idea how to escape this endless cycle of despair and defeat. Maybe, just maybe, someone out there can relate and offer some guidance. Or maybe it's all just too late for me...", 3);