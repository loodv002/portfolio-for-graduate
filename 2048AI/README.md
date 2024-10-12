# 2048 AI

## Run
```shell
$ python ./demo.py <ai model: 0-3>
```
e.g.: ```$ python ./demo.py 0``` will run the agent in `AI_0.py`。

## Algorithm Explanation
### AI_0
* Idea: Start from a given board state $S$ and make random moves until the game ends. By repeating this process multiple times, the average final score can indicate how good the starting state $S$ is.
* Algorithm: For a given board state, generate new subsequent states based on possible move directions. For each subsequent state, perform the evaluation mentioned above. Take the subsequent state with highest average final score as final decision.

### AI_1
* Idea: AI_0 spends too much time on unimportant states (see the PDF for a detailed explanation). Therefore, the number of random samples used to make a decision is no longer a fix value; instead, it is determined by the time consumed for a single sampling.
* Algorithm: Similar to AI_0, but each single-direction evaluation consumes the same amount of time. In other words, the longer it takes for a single sample, the fewer samples are conducted during the evaluation.

### AI_2
* Algorithm: Minimax (3 layers).
* The state evaluation heristic are derived from reference [2].

### AI_3
* Algorithm: Minimax with dynamic number of layers. The number of minimax layers is determined by the time spent on the previous evaluation (see the PDF for a detailed explanation).

## Performance

### Overall
|  | AI_0 | AI_1 | AI_2 | AI_3 |
| --- | --- | --- | --- | --- |
| average score | 35308.8 | 43374.7 | 43528.9 | 45827.7 |
| average step | 1782.3 | 2128.1 | 2135.7 | 2234.9 |
| average time/step | 0.246 | 0.256 | 0.043 | 0.183 |

# Max Block distribution
| percentage(%) | 512 | 1024 | 2048 | 4096 | 8192 |
| --- | --- | --- | --- | --- | --- |
| AI_0 | 2 | 16.6 | 62.6 | 18.8 | 0 |
| AI_1 | 0.6 | 8.2 | 57 | 34.2 | 0 |
| AI_2 | 0.6 | 12.4 | 51.2 | 34.8 | 1 |
| AI_3 | 1 | 9 | 49.4 | 40 | 0.6 |


## Reference
1. https://github.com/ronzil/2048-AI
2. https://github.com/ovolve/2048-AI