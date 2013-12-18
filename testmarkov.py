from app.brain import twitter, _get_tweet_texts
from app.brain.markov import Markov
import os

test_filepath = 'app/tests/markov.pickle'

#foo = twitter.tweets('frnsys', count=2000)
#t = _get_tweet_texts(foo)
t = [
        'The lion (Panthera leo) is one of the four big cats in the genus Panthera, and a member of the family Felidae. With some males exceeding 250 kg (550 lb) in weight, it is the second-largest living cat after the tiger. Wild lions currently exist in Sub-Saharan Africa and in Asia with an endangered remnant population in Gir Forest National Park in India, having disappeared from North Africa and Southwest Asia in historic times. Until the late Pleistocene, about 10,000 years ago, the lion was the most widespread large land mammal after humans. They were found in most of Africa, across Eurasia from western Europe to India, and in the Americas from the Yukon to Peru. The lion is a vulnerable species, having seen a possibly irreversible population decline of thirty to fifty percent over the past two decades in its African range. Lion populations are untenable outside designated reserves and national parks. Although the cause of the decline is not fully understood, habitat loss and conflicts with humans are currently the greatest causes of concern. Within Africa, the West African lion population is particularly endangered. Lions live for ten to fourteen years in the wild, while in captivity they can live longer than twenty years. In the wild, males seldom live longer than ten years, as injuries sustained from continual fighting with rival males greatly reduce their longevity. They typically inhabit savanna and grassland, although they may take to bush and forest. Lions are unusually social compared to other cats. A pride of lions consists of related females and offspring and a small number of adult males. Groups of female lions typically hunt together, preying mostly on large ungulates. Lions are apex and keystone predators, although they scavenge as opportunity allows. While lions do not typically hunt humans, some have been known to do so. Highly distinctive, the male lion is easily recognised by its mane, and its face is one of the most widely recognised animal symbols in human culture. Depictions have existed from the Upper Paleolithic period, with carvings and paintings from the Lascaux and Chauvet Caves, through virtually all ancient and medieval cultures where they once occurred. It has been extensively depicted in sculptures, in paintings, on national flags, and in contemporary films and literature. Lions have been kept in menageries since the time of the Roman Empire and have been a key species sought for exhibition in zoos over the world since the late eighteenth century. Zoos are cooperating worldwide in breeding programs for the endangered Asiatic subspecies.'
        ]
m = Markov(filepath=test_filepath)
m.train(t)
for i in range(10):
    print(m.generate())


try:
    os.remove(test_filepath)
except FileNotFoundError:
    pass