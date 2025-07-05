rm -rf allure-results allure-report
pytest
allure generate allure-results --clean -o allure-report
echo Allure HTML report generated at: allure-report/index.html
