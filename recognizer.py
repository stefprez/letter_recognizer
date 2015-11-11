#!/usr/bin/env python

import sys
import os


class Input(object):
    neurons = None

    def __init__(self, filename, desired=None, bias=None):
        if Input.neurons is None:
            Input.neurons = {'A': Neuron('A'),
                             'B': Neuron('B'),
                             'C': Neuron('C'),
                             'D': Neuron('D')}
        self.text = []
        self.filename = filename
        self.letter = desired
        self.invalid = False
        self.result = "Not Analyzed"
        self.nets = {'A': False, 'B': False, 'C': False, 'D': False}
        if desired is not None:
            self.desired = {'A': -1.0, 'B': -1.0, 'C': -1.0, 'D': -1.0}
            self.desired[desired] = 1.0
        else:
            self.desired = {'A': -1.0, 'B': -1.0, 'C': -1.0, 'D': -1.0}

        if bias is None:
            self.bias = 0
        else:
            self.bias = bias
        self.inputs = []

    def _add_line(self, line):
        self.text.append(line)

    def analyze(self):
        self._analyze_text()
        self.print_result()

    def train(self):
        self._train_net()
        self._check_results()

    def _reset_nets(self):
        self.nets = {'A': False, 'B': False, 'C': False, 'D': False}

    def _check_results(self):
        found = False
        self.invalid = False
        # print "Letter: {}".format(self.letter)
        for letter in self.nets:
            # print "Neuron: {}".format(letter)
            output = self.neurons[letter].analyze(self.inputs)
            desired = self.desired[letter]
            # print "Output: {}".format(output)
            # print "Desired: {}".format(desired)
            if output != desired:
                # print "Not equal"
                self.invalid = True
                self._reset_nets()
                return
            if self.nets[letter]:
                if found:
                    # "Multiple found"
                    self.invalid = True
                    self._reset_nets()
                    return
                else:
                    self.result = letter
                    found = True
        if not found:
            self.result = "Not Recognized"

    def _analyze_text(self):
        self._compute_inputs()
        self._update_results()

    def _update_results(self):
        found = False
        for letter, neuron in self.neurons.iteritems():
            if neuron.analyze(self.inputs) == 1:
                if found:
                    self._reset_nets()
                    found = False
                    break
                self.nets[letter] = True
                self.result = letter
                found = True
        if not found:
            self.result = "Not Recognized"

    def _compute_inputs(self):
        if not self.inputs:
            for line in self.text:
                for char in line:
                    if char == '.':
                        self.inputs.append(-1.0)
                    elif char == '#':
                        self.inputs.append(1.0)
                    else:
                        raise ValueError("_analyze_text error: invalid character",
                                         c, self.filename, self.text)
            self.inputs.append(self.bias)

    def _train_net(self):
        self._compute_inputs()
        for letter, neuron in self.neurons.iteritems():
            desired = self.desired[letter]
            neuron.train(self.inputs, desired)

    def print_result(self):
        for key, value in self.nets.iteritems():
            print key, value
        filename = self.filename.split("/")[-1]
        print "{0}: {1}".format(filename, self.result)

    def print_text(self):
        for line in self.text:
            print line

    def is_invalid(self):
        self._check_results()
        return self.invalid

    @staticmethod
    def read_file(filename, desired=None):
        new_input = Input(filename, desired)
        num_lines = 0
        with open(filename) as file:
            for line in file:
                num_lines += 1
                line = line.rstrip()
                if len(line) == 7:
                    new_input._add_line(line)
                else:
                    raise ValueError(
                        'read_file error: Invalid input line length.',
                        filename, num_lines, line)
        if num_lines == 9:
            return new_input
        else:
            raise ValueError('read_file error: Invald number of lines',
                             filename, num_lines)


class Neuron(object):
    alpha = 0.00001

    def __init__(self, letter):
        self.letter = letter
        self.weights = [1.0 for _ in range(64)]

    def _update_weight(self, inputs, desired):
        alpha = Neuron.alpha
        for i in range(0, 64):
            self.weights[i] += alpha * desired * inputs[i]

    def _bipolar_step(self, inputs):
        total = 0
        for i in range(len(inputs)):
            total += inputs[i] * self.weights[i]
        if total >= 0:
            return 1
        else:
            return -1

    def analyze(self, inputs):
        return self._bipolar_step(inputs)

    def train(self, inputs, desired):
        output = self._bipolar_step(inputs)
        while output != desired:
            self._update_weight(inputs, desired)
            output = self._bipolar_step(inputs)

    def print_weights(self):
        for weight in self.weights:
            print weight,
        print


def main():
    training()
    user_run()


def analyze_file(filename, desired=None):
    try:
        input_file = Input.read_file(filename, desired)
        input_file.analyze()
    except ValueError as e:
        # Error in read_file
        print e.args
        sys.exit(1)
    except StandardError as e:
        # Error in analyze
        print e.args
        sys.exit(1)


def user_run():
    stop = False
    while not stop:
        filename = raw_input("Please enter filename: ")
        if filename == 'stop':
            stop = True
            print "Goodbye"
        else:
            relative_path = "./input/"
            path = os.path.abspath("{0}{1}".format(relative_path, filename))
            analyze_file(path)


def training():
    input_files = get_input_files()
    finished = False
    counter = 0
    while not finished:
        counter += 1
        # if counter % 500 == 0:
        #     print counter
        for input_file in input_files:
            input_file.train()
        finished = input_files_valid(input_files)

    print "Training Complete: {}".format(counter)


def input_files_valid(input_files):
    for input_file in input_files:
        if input_file.is_invalid():
            return False
    # for letter, neuron in input_file.neurons.iteritems():
    #     neuron.print_weights()
    return True


def get_input_files():
    relative_path = "./training_samples/"
    files = os.listdir(relative_path)
    input_files = []

    for filename in files:
        path = os.path.abspath("{0}{1}".format(relative_path, filename))
        letter = str(filename[0])
        if letter == 'N':
            letter = None
        curr_file = Input.read_file(path, letter)
        input_files.append(curr_file)
    return input_files


if __name__ == '__main__':
    main()
