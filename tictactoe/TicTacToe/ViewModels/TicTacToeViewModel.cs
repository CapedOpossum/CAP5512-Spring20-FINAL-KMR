using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using TicTacToe.Models;

namespace TicTacToe.ViewModels
{
    public class TicTacToeViewModel : INotifyPropertyChanged
    {
        private string myVar = "non";

        public string Button1Text
        {
            get { return myVar; }
            set
            {
                myVar = value;
                NotifyOfPropertyChanged(nameof(Button1Text));
            }
        }

        public Command Button1Command
        {
            get
            {
                return new Command(o =>
                {
                    Console.WriteLine("Button pushed");
                    Button1Text = "New text";
                });
            }
        }

        private void NotifyOfPropertyChanged(string v)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(v));
        }

        public event PropertyChangedEventHandler PropertyChanged;
    }
}
