def test_list_remove():
    result=['建面 117-155㎡', '\n                        ', '建面 117-149㎡', '\n                        ', '建面 267-335㎡',
     '\n                        ', '建面 88㎡', '\n                        ', '建面 90-259㎡', '\n                        ',
     '建面 1460㎡', '\n                        ', '建面 377-388㎡', '\n                        ', '建面 55-175㎡',
     '\n                        ', '建面 415㎡', '\n                        ']
    remove_n(result)
    print(result)

def remove_n(result):
        for k in result:
            if '\n' in k:
                del result[result.index(k)]


if __name__ == '__main__':
    test_list_remove()