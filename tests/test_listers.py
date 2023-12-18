from candore.modules.api_lister import APILister


class TestLister:
    instance = APILister()

    def test_list_endpoints(self):
        # Mock the _apis() method to return sample data
        self.instance._endpoints = lambda: {
            "AK": {
                "methods": [
                    {"index": {"paths": ["GET /api/aks", "GET /api/aks/cvs"]}},
                    {"create": {"paths": ["POST /api/aks"]}},
                ]
            },
            "CV": {
                "methods": [
                    {"index": {"paths": ["GET /api/cvs/"]}},
                    {"delete": {"paths": ["DELETE /api/cvs"]}},
                ]
            },
            "PRODS": {
                "methods": [
                    {"index": {"paths": ["GET /api/prod_id/repos/"]}},
                    {"delete": {"paths": ["DELETE /api/prods"]}},
                ]
            },
        }

        expected_result = {
            "AK": ["/api/aks", "/api/aks/cvs"],
            "CV": ["/api/cvs/"],
            "PRODS": [],
        }

        # Call the list_apis method
        result = self.instance.lister_endpoints()

        # Assert that the result matches the expected output
        assert result == expected_result, "The API endpoints list differs"
