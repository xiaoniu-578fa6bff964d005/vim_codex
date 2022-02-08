import json

try:
    import vim
except:
    print("No vim module available outside vim")
    pass


import openai


class Config:
    def __init__(self):
        self.organization_id = ""
        self.secret_key = ""
        self.default_param = {
            #  "engine": "davinci-codex",
            "engine": "code-davinci-001",
            "max_generated_tokens": 64,
            "best_of": 1,
            "temperature": 0.0,
            "stop": None,
            "max_supported_input_length": 4096 - 64,
            "use_stream_feature": True,
        }


import collections.abc


def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def load_config():
    import os

    config_path = vim.eval(
        "get( g:, 'vim_codex_conf', '~/.config/vim_codex/vim_codex.conf' )"
    )
    config_path = os.path.expanduser(config_path)
    config = Config()
    if os.path.isfile(config_path):
        with open(config_path, "r") as f:
            config_json = json.loads(f.read())
        update(config.__dict__, config_json)
    return config


def load_openai_config(config):
    openai.organization = config.organization_id
    openai.api_key = config.secret_key


config = load_config()
load_openai_config(config)


def complete_input(input_prompt, param={}):
    param = dict(config.default_param, **param)

    assert (
        len(input_prompt) <= param["max_supported_input_length"]
    ), "input is too long."
    assert (
        len(input_prompt) + param["max_generated_tokens"] <= 4096
    ), "input is too long and response size is zero."

    response = openai.Completion.create(
        engine=param["engine"],
        prompt=input_prompt,
        best_of=param["best_of"],
        temperature=param["temperature"],
        max_tokens=param["max_generated_tokens"],
        stream=param["use_stream_feature"],
        stop=param["stop"],
    )
    return response, param


def create_completion(param={}):
    # read from current buffer
    vim_buf = vim.current.buffer

    row, col = vim.current.window.cursor  # row is 1-based, col is 0-based
    before = "\n".join(vim_buf[: row - 1] + [vim_buf[row - 1][:col]])
    after = "\n".join([vim_buf[row - 1][col:]] + vim_buf[row:])
    input_prompt = (after + before)[
        -config.default_param["max_supported_input_length"] :
    ]
    # compute response
    response, param = complete_input(input_prompt, param)
    if not isinstance(response, collections.abc.Generator):
        response = (response,)
    # write to buffer
    write_response_sequence(response, param)


def write_response_sequence(response, param):
    # output buffer
    for single_response in response:
        completion = single_response["choices"][0]["text"]
        write_response(completion)


def write_response(t):
    vim_buf = vim.current.buffer
    vim_win = vim.current.window

    row, col = vim_win.cursor
    current_line = vim_buf[row - 1]
    new_line = current_line[:col] + t + current_line[col:]

    def insert_blanks_at(i, num):
        if i == len(vim_buf):
            for _ in range(num):
                vim_buf.append("")
        else:
            vim_buf[i:i] = ["" for _ in range(num)]

    new_lines = new_line.split("\n")
    insert_blanks_at(row, len(new_lines) - 1)

    for row_i in range(len(new_lines)):
        vim_buf[row - 1 : row - 1 + len(new_lines)] = new_lines

    new_col = len(new_lines[-1]) - (len(current_line) - col)

    vim_win.cursor = (row + len(new_lines) - 1, new_col)
    #  Flush the vim buffer.
    vim.command("redraw")
