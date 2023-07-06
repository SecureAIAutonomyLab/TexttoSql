# FineTune GPT models 
This section of documentation outlines the steps to prepare the training data to be used for fine tuning.

## Installation
Only if you do not have already installed openai package. Run:

```
pip install --upgrade openai
```

## Setup API KEY
Setup an environmental variable with your openai API KEY 

```
export OPENAI_API_KEY="<OPENAI_API_KEY>"
```

## From CSV,XLSX,JSON to JSONL 
To prepare your data to the correct format, openai offers a tool to verify the data is well formated. 

```
openai tools fine_tunes.prepare_data -f <LOCAL_FILE>
```

Create guidelines for the formatting of prompts and SQL query completions, which may include the utilization of a  separator such as \n\n###\n\n in the prompts. 

Additionally, ensure that the completions commence with whitespace and conclude with either ### or a designated STOP keyword.

## Fine tune the model 
Bade models that you can fine tune are davinici, curie, babbage and ada.

```
openai api fine_tunes.create -t <TRAIN_FILE_ID_OR_PATH> -m <BASE_MODEL>
``` 

Output Example:
```
$ openai api fine_tunes.create -t dataset_prepared.jsonl -m davinci
Found potentially duplicated files with name 'dataset_prepared.jsonl', purpose 'fine-tune' and size 45937 bytes
file-WRQytgwjKLSMeYA3o8w8qvS5
Enter file ID to reuse an already uploaded file, or an empty string to upload this file anyway: 
Upload progress: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████| 45.9k/45.9k [00:00<00:00, 107Mit/s]
Uploaded file from dataset_prepared.jsonl: file-BnHwpVlUOkATUzPv5HmMN8AF
Created fine-tune: ft-dJnF64LOTZsvUgdAUuo869KX
Streaming events until fine-tuning is complete...

(Ctrl-C will interrupt the stream, but not cancel the fine-tune)
[2023-06-08 14:43:59] Created fine-tune: ft-dJnF64LOTZsvUgdAUuo869KX

```

To get the name of your fine tuned model, run below command and it will list all created fine tune models. 
```
# List all created fine-tunes
openai api fine_tunes.list
```
Output Example:
Name of model **"fine_tuned_model": "davinci:ft-utsa-2023-06-08-19-50-56"**
```
$ openai api fine_tunes.list
{
  "data": [
    {
      "created_at": 1686253439,
      "fine_tuned_model": "davinci:ft-utsa-2023-06-08-19-50-56",
      "hyperparams": {
        "batch_size": 1,
        "learning_rate_multiplier": 0.1,
        "n_epochs": 4,
        "prompt_loss_weight": 0.01
      }
```


## Use the fine tuned model 

```python
import openai
openai.Completion.create(
    model=FINE_TUNED_MODEL,
    prompt=YOUR_PROMPT)
```

## Credits
<b>Steps based on guidelines from:</b>
- [Openai](https://platform.openai.com/docs/guides/fine-tuning)