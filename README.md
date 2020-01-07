# SOCO-Core Python SDK
Python client to use SOCO answer-as-as-service platform.

## Install 
    pip install soco-core-python
    
## Quick Start

This following example can be found at: quick_start.py. To see more examples, check out /examples folder

First of all, register at https://app.soco.ai. After get your API_KEYs, you can setup a answer answer 
using 10 lines of code!
    
    from soco_core.soco_client import SOCOClient
    from soco_core.examples import load_example_frame_data
    
    ADMIN_API_KEY = '898706a0-ecb2-457d-8f89-eea1c406f0ca'
    a_client = SOCOClient(ADMIN_API_KEY)

    print("Add some data to the index")
    frames = load_example_frame_data('mr.sun')
    print("Loaded {} frames.".format(len(frames)))
    a_client.replace_index(frames, sync=True, db_encoder_id='bert-base-uncase-answer-squad-4head', batch_size=10)

    print("Make a query")
    QUERY_API_KEY = '727bb6b3-455c-4ee5-8f48-c2ab95837e56'
    q_client = SOCOClient(QUERY_API_KEY)
    responses = q_client.query("what is the distance from earth to sun?", 10)
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
