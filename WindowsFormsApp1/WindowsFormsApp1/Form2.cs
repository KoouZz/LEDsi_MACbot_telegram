using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp1
{
    public partial class Form2 : Form
    {
        public Form2(string login, string psw)
        {
            InitializeComponent();
            Form2_InitComp();
            this.Width = 800;
            this.Height = 600;
            this.StartPosition = FormStartPosition.CenterScreen;
            label2.Text = login;

        }

        private void Form2_Load(object sender, EventArgs e)
        {
            
        }

        public void label2_Click(object sender, EventArgs e)
        {

        }

        private void Form2_InitComp ()
        {
            //
            //label2
            //
            Label label2 = new Label();
            Controls.Add(label2);
            label2.Text = "Name";
            label2.Height = 30;
            label2.Width = 100;
            label2.Location = new Point(Left + 20, Top + 20);
            //
            //label3
            //
            Label label3 = new Label();
            Controls.Add(label3);
            label3.Text = "Fename";
            label3.Height = 30;
            label3.Width = 100;
            label3.Location = new Point(Left + 20, label2.Location.Y + label2.Height + 10);
            //
            //label4
            //
            Label label4 = new Label();
            Controls.Add(label4);
            label4.Text = "Login";
            label4.Height = 30;
            label4.Width = 100;
            label4.Location = new Point(Left + 20, label3.Location.Y + label3.Height + 10);
            //
            //label5
            //
            Label label5 = new Label();
            Controls.Add(label5);
            label5.Text = "E-mail";
            label5.Height = 30;
            label5.Width = 100;
            label5.Location = new Point(Left + 20, label4.Location.Y + label4.Height + 10);
            //
            //label6
            //
            Label label6 = new Label();
            Controls.Add(label6);
            label6.Text = "Password";
            label6.Height = 30;
            label6.Width = 100;
            label6.Location = new Point(Left + 20, label5.Location.Y + label5.Height + 10);
            //
            //textbox - name
            //
            TextBox name = new TextBox();
            Controls.Add(name);
            name.Size = new Size(250, 30);
            name.Location = new Point(label2.Location.X + label2.Width + 10, label2.Location.Y);
            //
            //textbox - fename
            //
            TextBox fename = new TextBox();
            Controls.Add(fename);
            fename.Size = new Size(250, 30);
            fename.Location = new Point(label3.Location.X + label3.Width + 10, label3.Location.Y);
            //
            //textbox - login
            //
            TextBox login = new TextBox();
            Controls.Add(login);
            login.Size = new Size(250, 30);
            login.Location = new Point(label4.Location.X + label4.Width + 10, label4.Location.Y);
            //
            //textbox - email
            //
            TextBox email = new TextBox();
            Controls.Add(email);
            email.Size = new Size(250, 30);
            email.Location = new Point(label5.Location.X + label5.Width + 10, label5.Location.Y);
            //
            //textbox - psw
            //
            TextBox psw = new TextBox();
            Controls.Add(psw);
            psw.PasswordChar = '*';
            psw.Size = new Size(250, 30);
            psw.Location = new Point(label6.Location.X + label6.Width + 10, label6.Location.Y);
            //
            //button1
            //
            Button button1 = new Button();
            Controls.Add(button1);
            button1.Text = "Registration";
            button1.Size = new Size(160, 30);
            button1.Location = new Point((psw.Location.X + psw.Width - label6.Location.X)/2 - button1.Width/2, label6.Location.Y + label6.Height + 10);
        }


    }
}
