Week 2

Attended this week's meeting: Yes

### Progress this week

GA Baseline Reproduction
- Successfully ran the py-ga-VRPTW project on Customized Data 100 customers
- Baseline result 12 vehicles total cost 63333.99
- Understood core GA functions ind2route decoding eval_vrptw evaluation cx_partially_matched crossover mut_inverse_indexes mutation

Battery Constraint E Constraint Implementation
- Added battery check logic to the ind2route function
- Added battery_capacity and battery_consumption_rate parameters to the data file
- Tested different battery capacities 10 30 50 100 and observed their impact on results

Experimental Results and Data Analysis
- Battery capacity 100 -> 12 vehicles cost 63333.99 constraint not activated
- Battery capacity 50 -> 69 vehicles cost 81285.61
- Battery capacity 30 -> 38 vehicles cost 66990.85
- Battery capacity 10 -> 101 vehicles cost 96066.39
- Generated comparison chart comparison_chart.png showing battery capacity impact on cost and vehicle count

Code and Documentation Management
- Uploaded complete GA code py-ga-VRPTW to src directory on GitHub
- Created and submitted experiment report docs/week2_report.md
- Created and submitted reflection document docs/week2_reflection.md
- Fixed the submodule issue where py-ga-VRPTW was not recognized as a normal folder

### Challenges and Blockers

Variable scope issue travel_distance was undefined due to inconsistent indentation in ind2route resolved by adjusting code structure

Python cache interference modified code did not take effect resolved by deleting __pycache__ folders

GitHub submodule issue py-ga-VRPTW was recognized as a submodule because it contained a git folder resolved by removing the git folder and recommitting

POMO method not started due to time constraints will prioritize next week


### Links

GitHub Repository https://github.com/Jiarui-Qin/FURP-2026-Jiarui-ROSBootcamp
Comparison Chart https://github.com/Jiarui-Qin/FURP-2026-Jiarui-ROSBootcamp/blob/master/src/py-ga-VRPTW/results/comparison_chart.png
data https://github.com/Jiarui-Qin/FURP-2026-Jiarui-ROSBootcamp/tree/master/src/py-ga-VRPTW/results