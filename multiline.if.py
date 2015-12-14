a = 1
b = 2
c = "a"

if not (
            isinstance(a, (int, float)) 
        and isinstance(b, (int, float)) 
        and isinstance(c, (int, float))):
    raise TypeError("Error!")
else:
    print("success!")


if __name__ == '__main__':
    my_x(a, 2, "x")