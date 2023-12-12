import pytest
import sys
import mandates


class TestMandates:
    @pytest.fixture(scope="class")
    def weeks(self):
        weeks = mandates.main(output_file="test_results.txt")
        return weeks

    @pytest.fixture(scope="class")
    def bois(self):
        bois = mandates.read_names("inputs/bois.txt")
        return bois

    def get_meeting_dict(self, weeks: list[list[set]], boi: str) -> dict:
        """
        Get a dictionary of bois and how many times they met with the given boi
        :param weeks: list of weeks
        :param boi: boi to check
        :return: dictionary of bois and how many times they met with the given boi
        """

        meetings = dict()
        for week in weeks:
            for pair in week:
                boi1, boi2 = pair
                if boi1 == boi:
                    if boi2 in meetings:
                        meetings[boi2] += 1
                    else:
                        meetings[boi2] = 1
                elif boi2 == boi:
                    if boi1 in meetings:
                        meetings[boi1] += 1
                    else:
                        meetings[boi1] = 1

        return meetings

    def test_groups_of_two_or_three(self, weeks: list[list[set]]):
        for week in weeks:
            for pair in week:
                assert len(pair) == 2 or len(pair) == 3

    def test_boi_only_once_per_week(self, weeks: list[list[set]], bois: list[str]):
        for boi in bois:
            met_with = self.get_meeting_dict(weeks, boi)

            for key in met_with:
                assert met_with[key] == 1

    def test_each_boi_every_week(self, weeks: list[list[set]], bois: list[str]):
        for boi in bois:
            for week in weeks:
                found = False
                for pair in week:
                    if boi in pair:
                        found = True
                        break
                assert found

    @pytest.mark.parametrize(
        argnames="weeks, bois_with_numbers, expected",
        argvalues=[
            ([], {}, []),
            (
                [[{0, 1}, {2, 3}]],
                {0: "a", 1: "b", 2: "c", 3: "d"},
                [[{"a", "b"}, {"c", "d"}]],
            ),
            (
                [[{0, 1}, {2, 3}], [{0, 2}, {1, 3}]],
                {0: "a", 1: "b", 2: "c", 3: "d"},
                [[{"a", "b"}, {"c", "d"}], [{"a", "c"}, {"b", "d"}]],
            ),
        ],
    )
    def test_transform_weeks(self, weeks, bois_with_numbers, expected):
        transformed_weeks = mandates.transform_weeks(weeks, bois_with_numbers)

        for week, expected_week in zip(transformed_weeks, expected):
            for pair, expected_pair in zip(week, expected_week):
                boi1, boi2 = pair
                assert boi1 in expected_pair
                assert boi2 in expected_pair

    def test_fill_week(self):
        assert 1 == 1

    def test_construct_graph(self):
        assert 1 == 1

    def test_read_names(self):
        assert 1 == 1

    def test_read_weeks(self):
        assert 1 == 1
