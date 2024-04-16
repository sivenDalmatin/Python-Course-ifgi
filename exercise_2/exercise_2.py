
def donuts(count):   
    answer= ""
    # Check if the input type equals an integer
    if type(count) == int:
        if count < 10:
            answer = f"Number of Donuts: {count}"
        else:
            answer = "Number of Donuts: many"
    else:
        answer = "Input has to be an Integer"
    return answer


def verbing(s):
    # if input ends with "ing" add "ly"
    if(s.endswith('ing')):
       s = s + 'ly'
    # else if input is at least 3 characters, add "ing"
    elif (len(s) >= 3):
        s = s + 'ing'
    # in other cases return just the input
    return s



def remove_adjacent(nums):
    # If list is emtpy, return info
    if not nums:
        return "List is empty"
    # transform input into set (set has no adjacents) and back to a list
    return list(set(nums))

def main():
    print('donuts')

    print(donuts(4))
    print(donuts(9))
    print(donuts(10))
    print(donuts("twentyone"))

    print('verbing')
    print(verbing('hail'))
    print(verbing('swiming'))
    print(verbing('do'))

    print('remove_adjacent')
    print(remove_adjacent([1, 2, 2, 3]))
    print(remove_adjacent([2, 2, 3, 3, 3]))
    print(remove_adjacent([]))

if __name__ == '__main__':
    main()
