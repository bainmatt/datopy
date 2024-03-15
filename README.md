# data-tools

Python tools for data retrieval, display, saving, and Jupyter notebook workflows.

*(Under Development)*

## Getting Started

### Installation

1. Clone the repo

```bash
$ git clone https://github.com/mattlabcode/data-tools.git
$ cd data-tools
```

2. Install dependencies

```bash
$ conda env create -f environment.yml
$ conda activate data-tools
```

### Downloading a particular module

Inside a notebook, run the following cell to import a module of interest (replacing the  “< >” placeholders with the desired inputs). Note that certain functions may require other scripts from the repo to run.

```python
# 1. Import urllib
import urllib.request

# 2. Set URL of module to import
script_url = "https://raw.githubusercontent.com/mattlabcode/data-tools/main/<script>.py"

# 3. Download the script
urllib.request.urlretrieve(script_url, "<script_name>.py")

# 4. Import the script
import <script_name>
```

Now you can use functions from `<script_name>`:

```python
<script_name>.<function_name>(<args>)
```

## Usage

*(Under Development: At the moment this is more of a wishlist than an overview of existing functionalities)*

1. **Notebook utilities**: Use `nb_utils.py` to save your Colab environment files to your mounted Google Drive from within a Colab notebook.
2. **Dataset pretty printing**: Use `display_dataset.py` to produce multiple parallel, informative displays of Pandas data frames and NumPy arrays for data exploration and inspection.
3. **Media scraping**: Use `media_scrape.py` to scrape media-related data from Spotify, IMDb, and Wikipedia.

## Examples

*(Under Development)*

*For more examples, please refer to [this](https://example.com/) (future) blog post.*

## Roadmap

- [ ] Complete implementation of (1-3) above

See the [open issues](https://github.com/mattlabcode/data-tools/issues) for a full list of proposed features (and known issues).

## License

This project is licensed under the MIT License.

## Contact

Project Link: https://github.com/mattlabcode/data-tools

