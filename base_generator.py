from abc import ABC, abstractmethod

class ProblemGenerator(ABC):
    """Abstract base class for math problem generators."""

    @abstractmethod
    def generate(self) -> dict:
        """
        Generates a math problem instance.

        Returns:
            dict: A dictionary containing:
                - 'problem_id': str — unique id, use helpers.jid()
                - 'operation': str (e.g., 'long_division')
                - 'problem': str (e.g., '123 / 4')
                - 'steps': list[str] — pipe-delimited step strings built with
                       helpers.step(op, ...), e.g. 'D|12|4|3'. Each step is an
                       op-code plus up to 4 payload fields (trailing empty
                       fields are trimmed). The last step must be exactly
                       'Z|<final_answer>'.
                - 'final_answer': str or int (e.g., '30 R3')

        Metadata: 'grade_level' and 'difficulty' are stamped centrally from
        curriculum.py after generate() returns (every generator class needs a
        CURRICULUM entry there). A generator may emit either key itself to
        override the table, e.g. difficulty computed from its operands.

        Op-code vocabulary: the scratchpad belongs to the model — new op-codes
        may be introduced freely; there is no fixed registry. Stay consistent
        within a generator, keep every step human-legible (the same cues a
        person would write on paper), and regenerate OPCODES.md
        (python tools/gen_opcode_legend.py) when introducing codes.
        """
        pass
