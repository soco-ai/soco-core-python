# SOCO-Core Python SDK
Python client to use SOCO answer-as-as-service platform.

## Install 
    pip install xxx
    
## Quick Start

This following example can be found at: quick_start.py. To see more examples, check out /examples folder

First of all, register at https://app.soco.ai. After get your API_KEYs, you can setup a answer answer 
using 10 lines of code!

    QUERY_API_KEY = '727bb6b3-455c-4ee5-8f48-c2ab95837e56'
    ADMIN_API_KEY = '898706a0-ecb2-457d-8f89-eea1c406f0ca'

    q_client = SOCOClient(QUERY_API_KEY)
    a_client = SOCOClient(ADMIN_API_KEY)

    print("## Add some data to the index")
    data = load_example_frame_data('mr.sun')
    a_client.append_to_index(data)

    print("## Wait for indexing is done ... ")
    a_client.wait_for_ready(check_frequency=2, timeout=10, verbose=False)

    print("## Make a query")
    responses = q_client.query("how many images", 10)
    SOCOClient.pprint(responses)
    
## Citation
If you use SOCO in research, we would love to be cited:

```latex
    @misc{soco2019engine,
      title={SOCO: Answer Engine Platform},
      author={Tiancheng Zhao and Kyusong Lee},
      howpublished={\url{https://github.com/ConvMind/soco-core-python}},
      year={2019}
    }
```
