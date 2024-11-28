# Rotating-Arrow-Game-AI
An AI that solves the [Rotating Arrow Game](https://github.com/EricL521/Rotating-Arrow-Game/), using [Keras_Core](https://github.com/keras-team/keras-core)

## Setup
Guide to installing repository and required packages

### Prerequisites
- Python 3.12.7
  - Project will not work on Python 3.13

### Quick Start
- Single command that installs project. Requires Python 3.12.7
  - Linux
    
    ```bash
    git clone https://github.com/EricL521/Rotating-Arrow-Game-AI.git && cd Rotating-Arrow-Game-AI && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
    ```
  - Windows
    
    ```cmd
    git clone https://github.com/EricL521/Rotating-Arrow-Game-AI.git && cd Rotating-Arrow-Game-AI && python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt
    ```

### Manual Installation
- Clone repository
  
  ```bash
  git clone https://github.com/EricL521/Rotating-Arrow-Game-AI.git
  ```
- Enter newly created folder
  
  ```bash
  cd Rotating-Arrow-Game-AI
  ```
- Create Python virtual environment
  
  ```bash
  python -m venv .venv
  ```
<a name="python-venv"></a>
- Activate Python virtual environment
  - Linux
    
    ```bash
    source .venv/bin/activate
    ```
  - Windows
    
    ```cmd
    .venv\Scripts\activate
    ```
- Download packages
  
  ```bash
  pip install -r requirements.txt
  ```

## Testing and Training
Guide to testing model, or training your own

### Prerequisites
- [Activate virtual environment](#python-venv)

### Testing
- Make sure `best_model.keras` is in base directory
- Run `test-ai.py` script
  
  ```bash
  python test-ai.py
  ```

### Training
- Change `data/config.yaml` if desired
- Generate new data points if needed

  ```bash
  python data/generate-data.py
  ```
- Train new model

  ```bash
  python train-ai.py
  ```
- Copy `model/best_model.keras` to base directory (i.e. `best_model.keras`) to [test](#testing)
