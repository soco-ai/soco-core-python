# SOCO-Core Python SDK
Python client to use SOCO answer-as-as-service platform.

## Install 
    pip install soco-core-python
    
## Quick Start

This following example can be found at: quick_start.py. To see more examples, check out /examples folder

First of all, register at https://app.soco.ai. After get your API_KEYs, you can setup a answer answer 
using a few lines of code!

First, import the SOCO client
    
    from soco_core.soco_client import SOCOClient
    from soco_core.examples import load_example_doc_data

Second add some data to the index

    a_client = SOCOClient(ADMIN_API_KEY)
    doc = load_example_doc_data('mr.sun')
    a_client.add_data([doc])

Third, publish the indeex

    a_client.abort() # abort any existing publish just in case.
    a_client.publish('bert-base-uncased', 'bert-base-uncase-ti-log-max-320head-snm',
                     publish_args={
                         "es_version": "tscore",
                         "num_shard": 6,
                         "encode_args": {"min_threshold": 1e-3, "top_k": 2000, "term_batch_size": 2000}
                     })

Now you are ready to query the index!

    q_client = SOCOClient(QUERY_API_KEY)
    responses = q_client.query("what is the distance from earth to sun?", 10)
    SOCOClient.pprint(responses)
    
    
## Citation
If you use SOCO in research, we would love to be cited:

```latex
    @misc{soco2019engine,
      title={SOCO: Answer Engine Platform},
      author={Tiancheng Zhao and Kyusong Lee},
      howpublished={\url{https://github.com/soco-ai/soco-core-python}},
      year={2019}
    }
```
