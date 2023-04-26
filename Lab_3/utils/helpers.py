from types import NoneType


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
            if type(v) in [int, float, complex, str, bool, NoneType]:
                items_repr += f"\t{dumps(k)}: {dumps(v)},\n"
                continue

            items_repr += f"\t{dumps(k)}: {{\n"

            for line in dumps(v).split("\n")[1:]:
                items_repr += f"{self.move_line(line, 1)}\n"

        return items_repr
