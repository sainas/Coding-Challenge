## Libraries Required
* sys
* numpy

## Repo directory structure
├── README.md
├── run.sh
├── src
│   └── prediction-validation.py
├── input
│   ├── actual.txt
│   ├── predicted.txt
│   └── window.txt
├── output
│   └── comparison.txt
└── insight_testsuite
    ├── run_tests.sh
    └── tests
        ├── test_1
        │   ├── input
        │   │   ├── actual.txt
        │   │   ├── predicted.txt
        │   │   └── window.txt
        │   └── output
        │       └── comparison.txt
        │
        └── my_dirty_data_test
            ├── input
            │   ├── actual.txt
            │   ├── predicted.txt
            │   └── window.txt
            └── output
                └── comparison.txt
				

## Testing
A dirty data is provide in the `my_dirty_data_test` folder to prove that my code can work well on the following condition:
* Wrong id
* Predicted price is empty
* Predicted price is not a digit
* Total predicted time is less than total actual time
* Stock ids are out of order. For a stock, the order of appearance in `actual.txt` and in `predicted.txt` are unrelated.



