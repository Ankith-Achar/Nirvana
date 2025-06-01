const mentalHealthQuotes =  [
    "Therapist: How do you feel? Me: With my hands, mostly.",
    "My brain has too many tabs open.",
    "I'm not lazy, I'm just in energy-saving mode.",
    "I'm fine. It's just my anxiety that’s on a rollercoaster.",
    "You don't have to be positive all the time. That’s how you get a cramp.",
    "If stress burned calories, I’d be a supermodel by now.",
    "I'm multitasking: I'm overthinking, overreacting, and overeating all at once.",
    "Self-care is drinking water and minding my own business.",
    "Therapy: because adulting is hard.",
    "Some days I amaze myself. Other days, I can’t find my phone... while I’m on it.",
    "The only running I do is running out of patience.",
    "I talk to myself because I need expert advice.",
    "Taking a mental health day… or decade.",
    "Trying to keep my anxiety and my coffee levels balanced. It’s a full-time job.",
    "My coping mechanism is memes.",
    "Deep breaths and Wi-Fi: essentials for modern survival.",
    "Normalize crying a little before doing literally anything.",
    "It’s not procrastination, it’s prioritizing my mental breakdowns.",
    "I'm not okay, but I'm okay with that.",
    "If mental health was visible, half the world would be wearing helmets.",
    "Self-care isn’t selfish. Unless you eat the last donut. Then it kinda is.",
    "Shout out to everyone who got out of bed today. You’re doing amazing.",
    "Therapy: because ‘suck it up’ isn’t a treatment plan.",
    "I’m trying to be the calm in the chaos… but the chaos is winning today.",
    "Just because I carry it well doesn’t mean it’s not heavy.",
    "I can’t brain today. I have the dumb.",
    "Mental health matters… even on Mondays.",
    "Don't judge someone’s story by the chapter you walked in on.",
    "Overthinking: my cardio for the day.",
    "Laughter is the best medicine—unless you have anxiety, then it's probably deep breathing.",
    "I’ve got 99 problems and most of them are made up scenarios in my head.",
    "Don’t mind me, I’m just arguing with my anxiety.",
    "Worrying works! 90% of the things I worry about never happen.",
    "I'm emotionally constipated. I haven't given a crap in days.",
    "My anxiety gives my depression a ride to work.",
    "Introverts unite... separately... in our own homes.",
    "You ever just stare at the wall and wonder if it’s staring back?",
    "My mood swings are powered by caffeine and existential dread.",
    "Me: ‘I need help.’ Also me: ‘I can do it myself!’",
    "Life tip: Don't believe everything you think.",
    "Anxiety: When you care too much about everything. Depression: When you stop caring at all. Me: Perfectly balanced, as all things should be.",
    "Being an adult is mostly just googling symptoms and crying a little.",
    "Therapy is expensive, but so is retail therapy. At least therapy doesn’t come with buyer’s remorse.",
    "I’m a big fan of naps, snacks, and not having a panic attack today.",
    "It’s okay to ask for help. Even Batman had Alfred.",
    "I have trust issues... with my own brain.",
    "Mindfulness is great. Until your mind is full.",
    "Healing is not linear. Sometimes it's just spiraling in a nicer pattern.",
    "Why cry in the club when you can cry in therapy?",
    "My trauma called. It said it’s not done with me yet."
  ];


function showRandomQuote() {
  const quote = mentalHealthQuotes[Math.floor(Math.random() * mentalHealthQuotes.length)];
  const quoteElement = document.getElementById("quote-text");
  if (quoteElement) {
    quoteElement.textContent = quote;
  }
}

// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
  showRandomQuote(); // Show one immediately
  setInterval(showRandomQuote, 5000); // Change every 10 seconds
});








