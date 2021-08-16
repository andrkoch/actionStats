from json import dumps, loads
from copy import deepcopy
from json.decoder import JSONDecodeError
from threading import Lock

lock = Lock()


class actionStats:
    """actionStats tracks actions and completion times and produces an average. It takes in
    and produces json serialized strings. See methods for format.

    Implimentation Assumptions
    This approach keeps a running summation of sample times and the number of samples.
    It assumes more updates will occur than statistics are requested. Thus it computes
    the averages on calls to getStats instead of on an addAction.

    This class is thread safe.


    """

    def __init__(self) -> None:

        # Used to store the action statistics.
        # Takes the form:
        #   { action -> (sampleSummation, numberSamples)}
        self.actionData = {}

    def addAction(self, jsonSerializedString: str) -> bool:
        """
            This function accepts a json serialized string of the form below and maintains an average time
            for each action.

        Args:
            jsonSerializedString (str): A json serialized string containing an action and a time.
                                        Two sample inputs:
                                            1) '{"action":"jump", "time":100}'
                                            2) '{"action":"run", "time":75}'

        Returns:
            bool: Returns True  - If a new action time pair is added.
                          False - If any error occurred.
        """
        try:
            deserializedActionDict = loads(jsonSerializedString)
        except (JSONDecodeError, TypeError):
            return False

        if type(deserializedActionDict) is not dict:
            return False

        # Retrieve the action and time. If the action and time
        # were not passed in correctly, do not process futher.
        actionType = deserializedActionDict.get("action")
        actionTime = deserializedActionDict.get("time")
        if type(actionType) is not str or type(actionTime) is not int:
            return False

        # Read and update the statistics for this action
        with lock:
            timeSummation, numberSamples = self.actionData.get(actionType, (0, 0))
            self.actionData[actionType] = (
                timeSummation + actionTime,
                numberSamples + 1,
            )
        return True

    def getStats(self) -> str:
        """
            Returns a serialized json array of the average time for each action stored by addAction

        Returns:
            str: A json serialized string of the form:
                 '[{"action":"jump", "avg":150},{"action":"run", "avg":75}]'
        """
        actionAverageTimeList = []

        # Make a copy to prevent holding a lock while processing the output
        # This assumes reducing blocking time is more important than memory utilization
        with lock:
            actionDataCopy = deepcopy(self.actionData)

        for actionName, statisticsData in actionDataCopy.items():
            actionAverageTimeList.append(
                {
                    "action": actionName,
                    "avg": (int)(statisticsData[0] / statisticsData[1]),
                }
            )
        return dumps(actionAverageTimeList)
