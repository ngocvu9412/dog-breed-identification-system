#!/usr/bin/env python
"""Generate the 20-breed corpus (M2).

One .md doc per breed with a fixed section structure:
Overview / Temperament / Health / Grooming / Exercise / Fun facts.
Static AKC-style breed knowledge, checked against public sources.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

BREEDS = {
    "golden_retriever": {
        "name": "Golden Retriever",
        "group": "Sporting",
        "overview": "A friendly, intelligent sporting breed developed in Scotland in the mid-19th century to retrieve shot waterfowl. Adults stand 55-61 cm and weigh 25-34 kg. The double coat is dense and water-repellent, in shades of gold.",
        "temperament": "Outgoing, eager to please, and gentle. Goldens are famously patient with children and friendly with strangers and other pets. High trainability has made them a top choice for service and therapy work.",
        "health": "Typical lifespan 10-12 years. Prone to hip and elbow dysplasia, certain cancers (hemangiosarcoma, lymphoma), progressive retinal atrophy, and hypothyroidism. Reputable breeders screen hips, elbows, eyes, and heart.",
        "grooming": "Brush two to three times per week; daily during spring and autumn shedding seasons. Bathe every 6-8 weeks. Check and clean ears weekly to prevent infections. Trim nails monthly.",
        "exercise": "Needs 1-2 hours of activity daily: walks, fetch, or swimming. Swimming is a signature activity because the breed was built for water retrieval. Mental exercise such as training games matters as much as physical work.",
        "facts": "Consistently among the most popular dog breeds in the United States. A soft mouth lets a Golden carry an egg without cracking it.",
    },
    "labrador_retriever": {
        "name": "Labrador Retriever",
        "group": "Sporting",
        "overview": "A muscular, friendly retriever developed in Newfoundland to haul nets and fish for fishermen. Adults stand 55-62 cm and weigh 25-36 kg. Short dense coat in black, yellow, or chocolate.",
        "temperament": "Sociable, high-spirited, and food-motivated. Labs mature slowly; adolescent energy can last until age three. Excellent with children, though their enthusiasm can knock over toddlers.",
        "health": "Typical lifespan 10-14 years. Watch for hip and elbow dysplasia, exercise-induced collapse, obesity, and progressive retinal atrophy. Ear infections are common in swimmers.",
        "grooming": "Low-maintenance coat: brush weekly with a rubber curry. Heavy shedding twice a year. Bathe every 6-8 weeks and dry ears thoroughly after swimming.",
        "exercise": "80 minutes to 2 hours daily. Fetch is the signature game; most Labs will retrieve indefinitely. Weight management depends on exercise because the breed is obesity-prone.",
        "facts": "The most popular dog breed in the United States for over 30 consecutive years per AKC registrations. Many guide dogs for the blind are Labs.",
    },
    "german_shepherd": {
        "name": "German Shepherd",
        "group": "Herding",
        "overview": "A large working breed standardized in Germany in 1899 by Max von Stephanitz for herding and utility work. Males stand 60-65 cm and weigh 30-40 kg. Medium-length double coat, most commonly black and tan.",
        "temperament": "Loyal, confident, and courageous. Naturally protective without excessive aggression when well socialized. Aloof with strangers until introduced. Bonds deeply to its person or family.",
        "health": "Typical lifespan 9-13 years. Prone to hip dysplasia, degenerative myelopathy, bloat, and exocrine pancreatic insufficiency. Breeding lines should be screened for hips and elbows.",
        "grooming": "Brush twice weekly; daily during the two heavy seasonal sheds. A year-round shedder. Bathe only every 2-3 months to preserve coat oils.",
        "exercise": "2 or more hours daily with a job to do: obedience, tracking, agility, or protection sports. A bored Shepherd invents destructive jobs. Mental stimulation is essential.",
        "facts": "The world's leading police and military dog. The movie star Rin Tin Tin was a German Shepherd found on a WWI battlefield.",
    },
    "french_bulldog": {
        "name": "French Bulldog",
        "group": "Non-Sporting",
        "overview": "A compact bat-eared companion breed developed in Paris in the 1800s from toy bulldogs. Weight under 14 kg; height about 28-33 cm. Smooth short coat in brindle, fawn, white, or cream.",
        "temperament": "Affectionate, adaptable, and quietly playful. They want to be with their person constantly and dislike being left alone. Alert enough to announce visitors but rarely noisy.",
        "health": "Typical lifespan 10-14 years. A brachycephalic (flat-faced) breed: heat intolerance and breathing difficulties are real risks. Most Frenchies cannot swim, and the vast majority of litters are delivered by C-section.",
        "grooming": "Minimal: weekly brushing and monthly baths. Clean the facial skin folds several times per week to prevent bacterial infections. Routine ear and nail care.",
        "exercise": "20-30 minutes daily in short walks. Never exercise in heat or humidity; the flat face makes them prone to heatstroke. Keep them lean.",
        "facts": "Overtook the Labrador as the most popular US breed in AKC registrations in 2022-2023. They snore loudly and often 'talk' to their owners.",
    },
    "poodle": {
        "name": "Poodle (Standard)",
        "group": "Non-Sporting",
        "overview": "An elegant water retriever originating in Germany over 400 years ago; the fancy clip historically protected joints and organs in cold water. Standards stand over 38 cm and weigh 20-32 kg.",
        "temperament": "Proud, extremely smart, and people-oriented. Standards are calmer than the smaller varieties. They learn quickly and need daily brain work or they invent mischief.",
        "health": "Typical lifespan 12-15 years, long for the size. Prone to hip dysplasia, epilepsy, Addison's disease, bloat, and sebaceous adenitis. Standard lines should be screened for Addison's history.",
        "grooming": "Professional grooming every 4-6 weeks is non-negotiable; the curly coat mats and grows continuously. Brush daily to weekly depending on clip. Ears need regular cleaning.",
        "exercise": "60-90 minutes daily. They excel at obedience, agility, and dock diving. Swimming is excellent low-impact exercise for the breed.",
        "facts": "Ranked second-smartest dog breed in Stanley Coren's working-intelligence ranking, behind only the Border Collie. Historically famous circus performers.",
    },
    "beagle": {
        "name": "Beagle",
        "group": "Hound",
        "overview": "A sturdy small hound bred in England for hunting rabbits in packs. Two size varieties: under 33 cm and 33-40 cm; weight 9-18 kg. Short coat, typically tricolor.",
        "temperament": "Merry, curious, and food-obsessed. Pack animals that prefer company of people or other dogs. The nose rules: a Beagle trailing a scent can go deaf to your calls.",
        "health": "Typical lifespan 12-15 years. Watch for epilepsy, hypothyroidism, intervertebral disc disease, cherry eye, and obesity. Long floppy ears need weekly cleaning.",
        "grooming": "Low: weekly brushing and ear cleaning, occasional baths. Moderate year-round shedding.",
        "exercise": "60-90 minutes daily including off-leash runs in secure areas. A fenced yard is strongly recommended because the breed follows its nose. Scent games are the best enrichment.",
        "facts": "Snoopy from the comic strip Peanuts is a Beagle. The breed's distinctive baying voice gave it the old French nickname 'begueule' (open throat).",
    },
    "rottweiler": {
        "name": "Rottweiler",
        "group": "Working",
        "overview": "A powerful guardian breed descended from Roman cattle dogs that settled in Rottweil, Germany. Males stand 61-69 cm and weigh 43-59 kg. Short black coat with rust markings.",
        "temperament": "Calm, confident, and courageously loyal. Well-socialized Rotties are gentle and playful at home, aloof with strangers, and slow to accept newcomers.",
        "health": "Typical lifespan 8-10 years. Prone to hip dysplasia, subaortic stenosis (heart), bloat, and bone cancer. Reputable breeders screen hearts and hips.",
        "grooming": "Easy coat care: weekly brushing, a few baths per year. Heavy seasonal shedding twice a year.",
        "exercise": "Two 20-40 minute sessions daily plus mental work. Carting, tracking, and obedience give this working dog a job.",
        "facts": "Rottweilers were butchers' dogs that pulled meat carts to market in Rottweil, hence the German nickname Metzgerhund (butcher's dog).",
    },
    "dachshund": {
        "name": "Dachshund",
        "group": "Hound",
        "overview": "A long-bodied scent hound (German for 'badger dog') bred to hunt badgers in their tunnels. Standards weigh 7-14 kg, miniatures under 5 kg. Three coat types: smooth, longhaired, wirehaired.",
        "temperament": "Brave to the point of comedy: a small dog bred to fight badgers underground. Stubborn, clever, and clingy with its person. Longhairs are often the calmest variety.",
        "health": "Typical lifespan 12-16 years, among the longest-lived breeds. The top risk is intervertebral disc disease: roughly a quarter of Dachshunds suffer a disc incident. Weight control and avoiding jumps help.",
        "grooming": "Smooths need a weekly wipe-down; longhairs brushing several times weekly; wirehairs hand-stripping a few times yearly. All need ear and nail care.",
        "exercise": "Two 30-minute walks daily plus play. Avoid rough jumping and long stair climbs to protect the spine. Scent work is the breed's original game.",
        "facts": "Waldi, a Dachshund, was the first official Olympic mascot (Munich 1972). Picasso's dog Lump appeared in several of his paintings.",
    },
    "german_shorthaired_pointer": {
        "name": "German Shorthaired Pointer",
        "group": "Sporting",
        "overview": "A versatile German hunting dog of the 1870s bred to point, retrieve on land and water, and track fur. Lean athletes: 21-32 kg, 53-64 cm. Liver or liver-ticked short coat.",
        "temperament": "High-energy dogs that bond intensely with their family. Without daily exercise they climb fences and dig craters. Friendly with strangers and other dogs.",
        "health": "Typical lifespan 12-14 years. Watch for hip dysplasia, bloat, and some cancers. Von Willebrand's disease (a bleeding disorder) appears in some lines.",
        "grooming": "The easiest wash-and-go coat: weekly rubber-curry brushing, occasional baths. Dry thoroughly after wet work.",
        "exercise": "2 or more hours of hard running daily for adults. Bred to hunt all day; a walk around the block is a warmup, not exercise. Field training or canicross are ideal.",
        "facts": "Webbed feet make them strong swimmers. The liver nose and noble head are the iconic look of an upland bird dog.",
    },
    "australian_shepherd": {
        "name": "Australian Shepherd",
        "group": "Herding",
        "overview": "A medium herding dog actually developed in the western United States from European stock brought by Basque shepherds. Weight 18-29 kg, height 46-58 cm. Merle, black, or red, with or without white and tan.",
        "temperament": "Brilliant, intense, and busy. Bred to control sheep all day; without livestock they may try to herd children and other pets. Reserved with strangers but not shy.",
        "health": "Typical lifespan 12-15 years. Eye defects (cataracts, collie eye anomaly) are the breed's main concern. The MDR1 gene mutation requires testing before certain drugs. Epilepsy appears in some lines.",
        "grooming": "Medium-maintenance double coat: brush 1-2 times weekly, more during the spring shed. Never shave; the double coat insulates against heat and cold.",
        "exercise": "1-2 hours daily of real work: agility, frisbee, or herding trials. Puzzle toys for rainy days.",
        "facts": "Despite the name, the breed has no Australian ancestry. Aussies dominate disc-dog and agility competitions.",
    },
    "shih_tzu": {
        "name": "Shih Tzu",
        "group": "Toy",
        "overview": "A toy companion ('little lion dog') bred in Tibetan monasteries and Chinese palaces. Weight 4-8 kg, height about 27 cm. Long flowing double coat in any color; often kept in a short puppy clip.",
        "temperament": "Affectionate lap dogs bred for centuries as palace companions. Alert and surprisingly sturdy for their size. They want to be near you, not to jog with you.",
        "health": "Typical lifespan 10-16 years. Brachycephalic: watch breathing in heat. Patellar luxation is common, and the prominent eyes are injury-prone. Dental disease is near-universal in the breed.",
        "grooming": "Full coat: daily brushing plus monthly professional grooming. Puppy clip: brushing every 2-3 days. Keep the eye area dry and clean to avoid staining and skin issues.",
        "exercise": "Short daily walks and indoor play; 30 minutes is plenty. They tolerate heat poorly, so walk early in summer.",
        "facts": "DNA studies place the Shih Tzu among the most ancient dog breeds. Tibetan 'little lion dogs' were palace gifts to Chinese emperors.",
    },
    "great_dane": {
        "name": "Great Dane",
        "group": "Working",
        "overview": "The 'Apollo of dogs', a giant breed (54-90 kg, 71-81 cm) developed in Germany from mastiff-type boar-hunting dogs. Short coat in fawn, brindle, black, blue, harlequin, or mantle.",
        "temperament": "Gentle giants that think they are lap dogs. Patient with children and friendly with strangers. Slow to mature: adolescent Danes are clumsy giant puppies.",
        "health": "Typical lifespan 7-10 years; giant breeds trade size for years. The number-one killer is bloat (gastric dilatation-volvulus); know the emergency signs. Also hip dysplasia and dilated cardiomyopathy.",
        "grooming": "Minimal: weekly brushing, occasional baths. A giant dog is a lot of surface to wipe after muddy walks.",
        "exercise": "Moderate: 30-60 minutes daily. No forced running before 18-24 months while joints grow. Soft bedding helps prevent pressure sores.",
        "facts": "Scooby-Doo and Marmaduke are Great Danes. The tallest dog ever recorded (Zeus, 111.8 cm at the shoulder) was a Great Dane.",
    },
    "border_collie": {
        "name": "Border Collie",
        "group": "Herding",
        "overview": "The world's premier sheep herder, developed in the Anglo-Scottish border country. Medium dog: 14-20 kg, 46-56 cm. The intense stare ('the eye') it uses to control sheep is the breed's signature.",
        "temperament": "The smartest known dog breed: a problem-solver and workaholic. Not a casual pet; without a job it will disassemble your house. Good with children when raised with them and given enough work, but their herding instinct may nip at running kids.",
        "health": "Typical lifespan 12-15 years. Collie eye anomaly, hip dysplasia, MDR1 drug sensitivity, and neuronal ceroid lipofuscinosis are the main concerns.",
        "grooming": "Moderate: brush 2-3 times weekly, more during shedding seasons.",
        "exercise": "2 or more hours daily PLUS mental work. In its element this breed herds sheep all day. Agility, flyball, or herding trials are ideal outlets.",
        "facts": "Ranked the smartest breed by Stanley Coren. Chaser the Border Collie learned the names of over 1,000 toys and fetched each by name, a milestone in animal-language research.",
    },
    "siberian_husky": {
        "name": "Siberian Husky",
        "group": "Working",
        "overview": "A medium endurance sled dog (16-27 kg, 51-60 cm) bred by the Chukchi people of Siberia to pull light loads over long distances. Thick double coat and facial mask; eyes brown or blue, or one of each.",
        "temperament": "Famously friendly and free-spirited: terrible guard dogs, excellent comedians. Pack animals that need company; a lone Husky is a howling escape artist.",
        "health": "Typical lifespan 12-14 years. Generally hardy. Watch for hip dysplasia, eye issues (cataracts, progressive retinal atrophy), and zinc-responsive dermatosis. Secure fencing is a health-grade necessity.",
        "grooming": "Heavy seasonal coat blows (clumps of undercoat) 1-2 times yearly: daily brushing then, weekly otherwise. Never shave a double coat.",
        "exercise": "1-2 hours daily minimum; they were bred to run vast distances pulling sleds. Off-leash recall is famously unreliable. Fenced yards and long lines.",
        "facts": "The 1925 serum run to Nome (the Balto story) was run by Husky teams; Togo covered the longest leg at 145 km. Husky blue eyes are not linked to health problems.",
    },
    "dobermann": {
        "name": "Dobermann",
        "group": "Working",
        "overview": "A German guardian breed created in the 1890s by tax collector Louis Dobermann for protection on his rounds. Sleek athletes: 27-45 kg, 61-72 cm. Black-and-rust most common; also red, blue, fawn.",
        "temperament": "Loyal, alert, and obedient to their family. Velcro dogs that want constant proximity. Modern breeding has made them far more companionable than their old fierce reputation.",
        "health": "Typical lifespan 10-12 years. The number-one breed risk is dilated cardiomyopathy; annual heart screening from age 3 is recommended. Also von Willebrand's disease, hip dysplasia, and bloat.",
        "grooming": "Minimal: weekly brush, occasional wipe-down. One of the lowest-maintenance working coats.",
        "exercise": "1-2 hours daily with intensity: running, obedience, or protection sports. They crave structured work with their person.",
        "facts": "Dobermanns served as US Marine war dogs in WWII; the first war-dog memorial on Guam honors a Dobermann named Kurt.",
    },
    "boxer": {
        "name": "Boxer",
        "group": "Working",
        "overview": "A muscular German breed of mastiff descent (Bullenbeisser) once used for hunting large game. Weight 25-32 kg, height 53-63 cm. Fawn or brindle with black mask; about one in five is born white.",
        "temperament": "The eternal puppy: playful well into old age. Patient with children, alert and wary of strangers. Brachycephalic build limits stamina in heat.",
        "health": "Typical lifespan 10-12 years. Elevated cancer rates, aortic stenosis, hip dysplasia, and bloat are concerns. White Boxers are often deaf.",
        "grooming": "Minimal: weekly brushing, occasional baths. White-marked dogs may need sunscreen on pink skin.",
        "exercise": "60-90 minutes daily; avoid heat. Puppy joints need care until 18 months.",
        "facts": "The name comes from the breed's habit of sparring with its front paws while playing. Boxers were among the first police dogs in Germany.",
    },
    "shetland_sheepdog": {
        "name": "Shetland Sheepdog",
        "group": "Herding",
        "overview": "The Sheltie, a small herder (5-11 kg, 33-41 cm) from Scotland's Shetland islands, bred to keep sheep out of crofts. It resembles a miniature Collie but is a separate breed. Rough double coat, commonly sable.",
        "temperament": "Sensitive, smart, and vocal. Devoted to their person and slow to warm to strangers. The bark announces everything.",
        "health": "Typical lifespan 12-14 years. Collie eye anomaly, dermatomyositis, MDR1 sensitivity, and patellar luxation are the main concerns. Thyroid issues appear with age.",
        "grooming": "Brush weekly, daily during seasonal sheds; the mane mats if neglected. Never shave the double coat.",
        "exercise": "60 or more minutes daily plus brain work. Agility is their sport: quick, biddable, and nimble.",
        "facts": "Shelties herd by darting at the heels of sheep. The breed excels at agility competitions worldwide.",
    },
    "cocker_spaniel": {
        "name": "Cocker Spaniel",
        "group": "Sporting",
        "overview": "A compact flushing spaniel from England and Wales, bred to flush woodcock (hence 'cocker'). Weight 12-14.5 kg, height 38-41 cm. Silky medium coat, solid or parti-color. The smallest sporting spaniel.",
        "temperament": "Merry, gentle, and people-soft. Sensitive to harsh correction; they wilt under yelling. Well-bred Cockers are sweet family dogs.",
        "health": "Typical lifespan 12-15 years. Ear infections are the signature issue because of the long pendulous ears; weekly cleaning is mandatory. Also hip dysplasia, progressive retinal atrophy, and later-life heart disease.",
        "grooming": "Significant: professional grooming every 6-8 weeks, brushing 2-3 times weekly. Keep ear canals clean and dry.",
        "exercise": "60 minutes daily with sniffing time. Scent games in long grass are pure joy for this flushing breed.",
        "facts": "Lady in Disney's Lady and the Tramp is a Cocker Spaniel; the film popularized buff-colored Cockers.",
    },
    "pug": {
        "name": "Pug",
        "group": "Toy",
        "overview": "An ancient Chinese toy breed ('much in little') later favored in Dutch and British courts. Weight 6-8 kg, height 25-28 cm. Smooth coat in fawn or black; curled tail and flat black mask.",
        "temperament": "Charming clowns bred for centuries to entertain. They thrive on attention and food equally. Minimal exercise needs, maximum companionship needs.",
        "health": "Typical lifespan 12-15 years. Brachycephalic: snoring and heat intolerance are normal features, heatstroke the danger. Prominent eyes are injury-prone; skin folds need care. Obesity is common.",
        "grooming": "Easy: weekly brushing, fold cleaning several times per week (keep the nose fold dry), monthly baths, monthly nails.",
        "exercise": "30-40 minutes daily in two short walks. Avoid heat and humidity entirely. Keep lean.",
        "facts": "A Pug is said to have saved William of Orange in 1572 by barking at an approaching Spanish ambush; the breed became the House of Orange's dog.",
    },
    "chihuahua": {
        "name": "Chihuahua",
        "group": "Toy",
        "overview": "The world's smallest breed, named for the Mexican state. Weight 1.5-3 kg, height 15-23 cm. Smooth or long coat in any color. The apple head with a molera (skull gap) is traditional.",
        "temperament": "Tremendous personality in a tiny frame: loyal to one person, suspicious of everyone else. Big-dog attitude in a 2-kg body. Poor tolerance for rough children.",
        "health": "Typical lifespan 14-17 years, among the longest-lived breeds. Fragile: top injuries are falls and being stepped on. Dental disease is near-universal in tiny crowded mouths.",
        "grooming": "Smooths: weekly wipe-down. Longhairs: weekly brushing. Daily dental care is ideal for this breed.",
        "exercise": "30 minutes daily; indoor play covers most needs. Avoid rough play with large dogs.",
        "facts": "The smallest dog ever recorded, Milly the Chihuahua, stood 9.65 cm tall. The breed descends from the Techichi kept by Toltec civilizations.",
    },
    "yorkshire_terrier": {
        "name": "Yorkshire Terrier",
        "group": "Toy",
        "overview": "A tiny terrier (2-3 kg) from Yorkshire, England, bred in the 1800s to catch rats in textile mills. Fine silky steel-blue-and-tan coat that grows continuously and resembles human hair.",
        "temperament": "Feisty, brave, and bossy in a lap-dog body. Devoted to their person, wary of strangers and other dogs. True terrier spirit.",
        "health": "Typical lifespan 13-16 years. Luxating patellas, collapsing trachea (use a harness, never a collar), puppy hypoglycemia, and dental disease.",
        "grooming": "High: a full coat needs daily brushing; most owners keep a puppy cut brushed every 2-3 days. Regular dental care is essential.",
        "exercise": "Two short walks daily plus indoor play; 30 minutes total is plenty.",
        "facts": "Smoky the Yorkshire Terrier ran telegraph wire through a drainpipe in WWII Luzon and is credited with 12 combat missions, earning 8 battle stars.",
    },
    "pomeranian": {
        "name": "Pomeranian",
        "group": "Toy",
        "overview": "A tiny spitz breed (1.4-3.2 kg) from Pomerania, downsized from sled dogs in the 1800s; Queen Victoria popularized the small type. Profuse double coat, orange-red most iconic.",
        "temperament": "Confident, curious, and extroverted. Alert watchdogs that bark readily. They forget their size and will challenge dogs 20 times their mass.",
        "health": "Typical lifespan 12-16 years. Patellar luxation, collapsing trachea (harnesses over collars), alopecia X, and dental disease.",
        "grooming": "Brush 2-3 times weekly with a pin brush; the thick undercoat mats. Never shave: the coat may not regrow properly. Daily dental care.",
        "exercise": "30 minutes daily in short sessions; indoor play works. Watch for overheating in the thick coat.",
        "facts": "Two Pomeranians were among the survivors of the Titanic sinking in 1912, carried off in lifeboats.",
    },
    "boston_terrier": {
        "name": "Boston Terrier",
        "group": "Non-Sporting",
        "overview": "The 'American Gentleman': a tuxedo-marked breed developed in Boston in the 1870s from Bulldog and the now-extinct White English Terrier. Weight 4.5-11 kg; height 38-43 cm at the withers.",
        "temperament": "Gentle, friendly, and eager to please. Sensitive to tone of voice; they respond best to positive methods. Playful well into adulthood.",
        "health": "Typical lifespan 11-13 years. Brachycephalic: heat intolerance and snoring. Patellar luxation, prominent-eye injuries, and allergies.",
        "grooming": "Minimal: weekly brushing, facial fold cleaning, regular nail care. White markings can collect tear stains.",
        "exercise": "30-45 minutes daily; avoid heat. The short face limits exertion in warm weather.",
        "facts": "The AKC's first homegrown American breed, recognized in 1893.",
    },
}


def write_corpus():
    os.makedirs(OUT, exist_ok=True)
    for slug, facts in BREEDS.items():
        name = facts["name"].strip()
        group = facts.get("group", "").strip()
        lines = [f"# {name}", ""]
        if group:
            lines.append(f"Breed group: {group}.")
            lines.append("")
        for section in ("overview", "temperament", "health", "grooming", "exercise", "facts"):
            val = facts.get(section)
            if not val:
                continue
            title = "Fun facts" if section == "facts" else section.capitalize()
            lines.append(f"## {title}")
            lines.append(val)
            lines.append("")
        path = os.path.join(OUT, slug + ".md")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines))
        print(f"  wrote {slug}.md")


if __name__ == "__main__":
    write_corpus()
    print(f"corpus dir: {OUT}")
    print(f"breeds: {len(BREEDS)}")