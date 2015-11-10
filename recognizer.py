#!/usr/bin/env python

import sys


class Input(object):
    neurons = {'A': Neuron(), 'B': Neuron(),
               'C': Neuron(), 'D': Neuron()}

    def __init__(self, filename, desired=None, bias=None):
        self.text = []
        self.filename = filename
        self.desired = desired
        self.result = "Not Analyzed"
        self.nets = {'A' = False, 'B' = False, 'C' = False, 'D' = False}
        self.inputs = []
        if desired is None:
            self.desired = {'A' = 0.0, 'B' = 0.0, 'C' = 0.0, 'D' = 0.0}
            elif
        if bias is None:
            self.bias = 0
        else:
            self.bias = bias

    def _add_line(self, line):
        self.text.append(line)

    def analyze(self):
        if self.desired is None:
            self._analyze_text()
        else:
            self._train_net()
        nets = self.nets
        found = False
        for key in nets:
            if nets[key]:
                if found:
                    raise StandardError('analyze error: Multiple true nets',
                                        nets, text)
                else:
                    self.result = key
                    found = True
        if not found:
            self.result = "Not Recognized"

    def _analyze_text(self):
        self._compute_inputs()
        self._update_results()

    def _update_results(self):
        raise NotImplementedError()

    def _compute_inputs(self):
        inputs = self.inputs
        for line in self.text:
            for char in line:
                if char == '.':
                    inputs.append(-1.0)
                elif char == '#':
                    inputs.append(1.0)
                else:
                    raise ValueError("_analyze_text error: invalid character",
                                     c, self.filename, self.text)

        inputs.append(self.bias)

    def _update_weight(self):
        raise NotImplementedError()

        for letter, neuron in Input.neurons:
            pass
        alpha = Input.alpha
        inputs =  # Not sure what this is yet...

        desired = 1  # 1 or 0 I think...
        weights = Input.weights

        for i in range(len(weights)):
            weights[i] = weights[i] + (alpha * desired * inputs[i])

    def _train_net(self):
        raise NotImplementedError()

        # Loop through each neuron

        # Train each neuron

    def print_result(self):
        print "{0}: {1}".format(self.filename, self.result)

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
    alpha = 0.1

    def __init__(self):
        self.weights = []


def main():
    training()
    # user_run()


def analyze_file(filename, desired=None):
    try:
        input_file = Input.read_file(filename, desired)
        input_file.analyze()
        input_file.print_result()
    except ValueError as e:
        # Error in read_file
        print e.args
    except StandardError as e:
        # Error in analyze
        print e.args


def user_run():
    stop = False
    while not stop:
        filename = raw_input("Please enter filename: ")
        if filename == 'stop':
            stop = True
            print "Goodbye"
        else:
            analyze_file(filename)


def training():
    files = os.listdir('./input/')
    for filename in files:
        analyze_file(filename, str(filename[0]))

    print 'training() not complete'  # print weights?
    for weight in Input.weights:
        print weight


if __name__ == '__main__':
    main()
