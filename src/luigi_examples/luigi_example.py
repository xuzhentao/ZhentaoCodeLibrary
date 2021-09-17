import time

import luigi


class PrintWord(luigi.Task):
    path = luigi.Parameter()
    word = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(self.path)

    def run(self):
        print("--------sleeping--------")
        time.sleep(30)
        with open(self.path, 'w') as fh:
            fh.write(self.word)


class myHelloWorld(luigi.Task):
    name = luigi.Parameter(default="mydefaultfolder")

    def requires(self):
        return [PrintWord(path="{}_hello.txt".format(self.name), word="hello_zhentao"),
                PrintWord(path="{}_world.txt".format(self.name), word="world_zhentao"), ]

    def output(self):
        return luigi.LocalTarget("{}_helloworld.txt".format(self.name))

    def run(self):
        word1 = None
        word2 = None

        with open(self.input()[0].path, 'r') as hello_hdr:
            word1 = hello_hdr.read()

        with open(self.input()[1].path, 'r') as world_hdr:
            word2 = world_hdr.read()

        with open(self.output().path, 'w') as output_hdr:
            output_hdr.write("{}+{}".format(word1, word2))


if __name__ == "__main__":
    luigi.run(main_task_cls=myHelloWorld)
