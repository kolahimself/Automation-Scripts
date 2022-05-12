def loading(height, unit_weight, factor):
    """
    Function that evaluates the dead load of a structural member,
    given it's height, or thickness as case may be,
    :param height: The given effective height of the structural member or wall partition
    :param unit_weight: The unit weight of the member in kn/m2
    :param factor: The Dead Load factor, as conservative design specified in respective codes.
    :return: height x unit_weight
    """
    load = float(height * unit_weight * factor)
    return load


def main():
    member_height = float(input('Enter the Member/Wall Height in metres (m):'))
    member_weight = float(input('Enter the Unit weight of the Member in kN per square area:'))
    member_sdead = float(input('Enter the value of super dead load or extra finishes.'))
    dl_factor = float(input('Enter the Dead Load factor as recommended by your Design Code:'))
    load = loading(member_height, member_weight + member_sdead, dl_factor)
    print(f"The Dead load per metre run is {round(load, 2)} KN per metre run")


main()
