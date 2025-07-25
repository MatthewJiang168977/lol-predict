# from collections import defaultdict

# sentences = [
#   "I love roses",
#   "Roses are the best",
#   "Roses are red violets are blue"
# ]
# def word_frequency(sentences):
#     words = defaultdict(int)
#     for s in sentences: 
#         word = ''
#         i = 0
#         while i < len(s): 
#             j = i
#             while j < len(s) and s[j].isalpha(): 
#                 word+= s[j].lower()
#                 j += 1
#             words[word] += 1
#             word = ''
#             i = j + 1
#     #print(words)
    
#     flipped = defaultdict(list)
#     for word, freq in words.items():
#         flipped[str(freq)].append(word)
#     return flipped

# print(word_frequency(sentences))



# def reverse_str(string): 
#     rev = string[::-1]
#     print(rev)
#     rev1 = "" 
#     for i in range(len(string)-1,-1,-1):
#         rev1 += string[i]
#     print(rev1)
#     return

# print(reverse_str("hello"))
nums = [1,2,3]
print(len(nums))
for i in range(0,len(nums)):
    # print(nums[i])
    print(i)