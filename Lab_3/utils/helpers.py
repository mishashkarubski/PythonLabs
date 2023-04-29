from types import NoneType, CellType


class Formatter:

    @staticmethod
    def move_line(string, indent):
        """

        :param string:
        :param indent:
        :return:
        """
        return "\t" * indent + string

    def to_json(self, obj, dumps):
        """

        :param obj:
        :param dumps:
        :return:
        """
        items_repr = ""

        for k, v in obj.items():
            if type(v) in [int, float, complex, str, bool, type(Ellipsis), NoneType]:
                items_repr += f"\t{dumps(k)}: {dumps(v)},\n"
                continue

            items_repr += f"\t{dumps(k)}: {{\n"

            try:
                dumps(v).split()
            except:
                print()
                print(v)

            for line in dumps(v).split("\n")[1:]:
                items_repr += f"{self.move_line(line, 1)}\n"

        return items_repr
