import asyncio

from iBott import OrchestratorConnectionError


class Log:
    """
    This class is used to log messages in the Orchestrator console.
    Arguments:
        robot: The robot object.

    """

    def __init__(self, robot):
        self.robot = robot

    def debug(self, log: str):
        """
        Send debug trace to ochestrator
        Arguments:
            log: The log message.
        Returns:
            None
        """
        log_type = 'debug'
        asyncio.run(self.send(log, log_type=log_type))

    def trace(self, log: str):
        """
        Send trace to ochestrator
        Arguments:
            log: The log message.
        Returns:
            None
        """
        log_type = 'log'
        asyncio.run(self.send(log, log_type=log_type))

    def info(self, log: str):
        """
        Send info trace to orchestrator
        Arguments:
            log: The log message.
        Returns:
            None
        """
        log_type = 'info'
        asyncio.run(self.send(log, log_type=log_type))

    def system_exception(self, error: str):
        """
        Send systemException trace to orchestrator
        Arguments:
            error: The error message.
        Returns:
            None
        """
        log_type = 'systemException'
        asyncio.run(self.send(error, log_type=log_type))

    def business_exception(self, error: str):
        """
        Send businessException trace to orchestrator
        Arguments:
            error: The error message.
        Returns:
            None
        """
        log_type = 'businessException'
        asyncio.run(self.send(error, log_type=log_type))

    async def send(self, log: str, log_type: str):
        """
        Async function to send logs to orchestrator
        Arguments:
            log: The log message.
            log_type: The log type.
        Returns:
            None
        Raise:
            OrchestratorConnectionError: If the connection with the orchestrator is not established.
        """
        if not self.robot.debug:
            try:
                await self.robot.__send_message(log, log_type=log_type)
            except:
                raise OrchestratorConnectionError("Orchestrator is not connected")
        else:
            print(f'{log_type}: {log}')